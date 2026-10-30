class AMDataChecker:
    def get_str_keypath(self, key: str = '') -> str:
        if self.amdata._pre_keylist:
            keypath = '.'.join(self.amdata._pre_keylist)
            if key:
                keypath += f'.{key}'
        else:
            keypath = key
        return keypath

    def raise_lxm_error(
        self,
        _exception: Exception,
        fmt_str: str,
        names: set[str] | list[str],
        **kwargs
    ) -> None:
        sep = ','
        comma_list_names = sep.join([
            f'{self.get_str_keypath(n)!r}'
            for n in sorted(names)
        ])
        plurial = 's' if sep in comma_list_names else ''
        raise _exception(
            fmt_str.format(
                plurial=plurial,
                names=comma_list_names,
                **kwargs
            )
        )

    def raise_kpse_error(
        self,
        _exception: Exception,
        fmt_str: str,
        _sub_exception: Exception | None = None,
        **kwargs
    ) -> None:
        if _sub_exception is None:
            etype = None
        else:
            etype = type(_sub_exception).__name__
            fmt_str += ': (sub){etype}: {e}'

        raise _exception(
            fmt_str.format(
                keypath=self.get_str_keypath(),
                etype=etype,
                e=_sub_exception,
                **kwargs
            )
        )

    def check_main_blocks(self, tolerent: bool) -> None:
        block_names_used = set(self.amdata._yaml_raw_data)

        if not self.amdata._mandatory_block_names <= block_names_used:
            self.raise_lxm_error(
                _exception=ValueError,
                fmt_str='Missing mandatory main block{plurial}: {names}.',
                names=self.amdata._mandatory_block_names - block_names_used,
            )

        if not tolerent and not block_names_used <= self.amdata._all_block_names:
            self.raise_lxm_error(
                _exception=KeyPathError,
                fmt_str='Unsupported main block{plurial}: {names}.',
                names=block_names_used - self.amdata._all_block_names,
            )

    def check_keys(self) -> None:
        self.amdata._current_keys_allowed = set(
            self.amdata._main_parsers[self.amdata._pre_keylist]
        )

        if self.amdata._pre_keylist in self.amdata._main_alts:
            self.amdata._current_alts = self.amdata._main_alts[
                self.amdata._pre_keylist
            ][TAG_ALTERNATIVES]
        else:
            self.amdata._current_alts = []

        self.amdata._current_status = self.amdata._main_status[
            self.amdata._pre_keylist
        ]

        self._check_legal_keys()
        self._check_no_alt_keys()
        self._check_manda_keys()

    def _check_legal_keys(self) -> None:
        if not self.amdata._current_keys_used <= self.amdata._current_keys_allowed:
            self.raise_lxm_error(
                _exception=KeyPathError,
                fmt_str='Illegal key{plurial}: {names}.',
                names=self.amdata._current_keys_used - self.amdata._current_keys_allowed,
            )

    def _check_no_alt_keys(self) -> None:
        illegal_couples = set()
        for alt_couple in self.amdata._current_alts:
            if alt_couple == (alt_couple & self.amdata._current_keys_used):
                illegal_couples.add(' vs '.join(sorted(alt_couple)))

        if illegal_couples:
            self.raise_lxm_error(
                _exception=KeyPathError,
                fmt_str='Illegal couple{plurial} of keys found: {names}.',
                names=illegal_couples,
            )

    def _check_manda_keys(self) -> None:
        mandatory_keys = set()
        for k, v in self.amdata._current_status.items():
            if k in SPECIAL_KEYS:
                continue
            if v[TAG_IS_MANDATORY]:
                mandatory_keys.add(k)

        if not mandatory_keys <= self.amdata._current_keys_used:
            self.raise_lxm_error(
                _exception=KeyPathError,
                fmt_str='Missing mandatory key{plurial}: {names}.',
                names=mandatory_keys - self.amdata._current_keys_used,
            )


# ------------------ #
# -- AMDATA CLASS -- #
# ------------------ #

MULTI_KEYPATH_TYPE = None | str | list[str]
PARSER_TYPE = (
    Callable[[object], object]
    | Callable[[object, object], object]
)


class AMData:

    @classmethod
    def new_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(
        self,
        flavour: str,
        parent: Path,
    ) -> None:
        self._checker = AMDataChecker(self)
        self.flavour = flavour
        self.parent = parent

    @property
    def flavour(self) -> str:
        return self._flavour

    @flavour.setter
    def flavour(self, flavour: str) -> None:
        if flavour not in ALL_FLAVOURS:
            raise ValueError(f'unknow flavour {flavour!r}.')

        self._flavour = flavour
        self._flavour_specs = ALL_FLAVOURS[flavour]

        self._all_block_names = set()
        self._mandatory_block_names = set()

        for bname in self._flavour_specs:
            self._all_block_names.add(bname)
            if self._flavour_specs[bname][TAG_IS_MANDATORY]:
                self._mandatory_block_names.add(bname)

    @property
    def parent(self) -> Path:
        return self._parent

    @parent.setter
    def parent(self, parent: Path) -> None:
        if not parent.is_dir():
            raise IOError(f"Missing folder '{parent}'.")

        yaml_file = parent / TAG_ABOUT_YAML
        if not yaml_file.is_file():
            raise IOError(f"Missing file '{yaml_file}'.")

        self._parent = parent
        self.yaml_file = yaml_file

    def build(self, tolerent: bool = True) -> benedict:
        self._full_data_keypaths = []
        self._yaml_raw_data = safe_load(self.yaml_file.read_text())

        if not isinstance(self._yaml_raw_data, dict):
            dtype = type(self._yaml_raw_data).__name__
            raise ValueError(
                f'{TAG_ABOUT_YAML!r} file must use '
                f'a main dictionary: {dtype!r} found.'
            )

        self._pre_keylist = []
        self._checker.check_main_blocks(tolerent)

        data = dict()
        for block, content in self._yaml_raw_data.items():
            if tolerent and block not in self._all_block_names:
                continue

            self._pre_keylist = [block]
            specs = self._flavour_specs[block]

            self._main_parsers = specs[TAG_BLOCK_PARSERS]
            self._main_status = specs[TAG_BLOCK_STATUS]
            self._main_alts = specs[TAG_BLOCK_ALTS]

            data[block] = self._recu_build(content)

        self.data = benedict(data)

    def _recu_build(self, raw_data: dict | list) -> dict:
        if isinstance(raw_data, list):
            datatype = self._this_data_type()
            if datatype != TAG_LIST:
                self._checker.raise_kpse_error(
                    _exception=ValueError,
                    fmt_str=f'Block {self._checker.get_str_keypath()!r} does not expect a list of data to parse.',
                )
            return self._build_list(raw_data)

        elif isinstance(raw_data, dict):
            return self._recu_build_dict(raw_data)

        else:
            self._checker.raise_kpse_error(
                dtype=type(raw_data).__name__,
                _exception=ValueError,
                fmt_str='Unsupported YAML content with Python type {dtype!r}. See key {keypath!r}.',
            )

    def _build_list(self, raw_data: list) -> list:
        self._update_full_data_keypaths()
        data = []
        parser_module = self._this_parser_module()

        for pos, rd in enumerate(raw_data, start=1):
            try:
                data.append(
                    self._get_parsed_data(
                        raw_data=rd,
                        parser_module=parser_module,
                    )
                )
            except Exception as e:
                self._checker.raise_kpse_error(
                    _sub_exception=e,
                    pos=pos,
                    _exception=ParsingError,
                    fmt_str=f'Block {self._checker.get_str_keypath()!r} has invalid item list data at position {{pos}}: {{etype}}: {{e}}',
                )
        return data

    def _recu_build_dict(self, raw_data: dict) -> dict:
        data = dict()
        self._current_keys_used = set(raw_data)
        self._checker.check_keys()

        for key, val in raw_data.items():
            self._pre_keylist.append(key)
            datatype = self._this_data_type()

            if datatype is None:
                new_val = self._recu_build(val)
            elif datatype == TAG_LIST:
                new_val = self._build_list(val)
            else:
                self._update_full_data_keypaths()
                new_val = self._get_parsed_data(
                    raw_data=val,
                    parser_module=self._this_parser_module(),
                )

            data[key] = new_val
            self._pre_keylist.pop(-1)

        return data

    def _get_parsed_data(self, raw_data: object, parser_module: ModuleType) -> object:
        if parser_module == str:
            if not isinstance(raw_data, str):
                raise ParsingError(f'{raw_data!r} is not a string.')
            return raw_data

        amdata_use, _ = self._this_amdata_use()
        try:
            if amdata_use:
                return parser_module.parse(amdata=self, data=raw_data)
            return parser_module.parse(raw_data)
        except Exception as e:
            self._checker.raise_kpse_error(
                _exception=ParsingError,
                fmt_str=f'Invalid data {raw_data!r}',
                _sub_exception=e,
            )

    def _update_full_data_keypaths(self) -> None:
        self._full_data_keypaths.append(self._checker.get_str_keypath())

    def _get_current_metadata(self, key: str) -> dict:
        return self._main_parsers[self._pre_keylist][key]

    def _this_data_type(self) -> str:
        return self._main_parsers[self._pre_keylist].get(TAG_DATATYPE, None)

    def _this_parser_module(self) -> ModuleType:
        return self._get_current_metadata(TAG_PARSER)

    def _this_amdata_use(self) -> tuple[bool, bool | None]:
        return self._get_current_metadata(TAG_AMDATA_USE)

    def _this_use_post(self) -> bool:
        return self._get_current_metadata(TAG_USE_POST)

    def _iter_keypath(self, keypath: MULTI_KEYPATH_TYPE = None) -> Any:
        if keypath is None:
            keypaths_wanted = self._full_data_keypaths
        elif isinstance(keypath, str):
            keypaths_wanted = [keypath]
        else:
            keypaths_wanted = keypath

        for kp in keypaths_wanted:
            if kp not in self._full_data_keypaths:
                raise KeyPathError(f'Broken keypath {kp!r}.')
            yield (
                kp,
                self.data[kp],
                self._main_parsers[kp][TAG_PARSER]
            )

    def standardize(self, keypath: MULTI_KEYPATH_TYPE = None) -> None:
        self.std_yaml_data = benedict()
        for kp, val, parser_module in self._iter_keypath(keypath):
            if parser_module == str:
                std_yaml_val = val
            else:
                std_yaml_val = parser_module.write(val)
            self.std_yaml_data.set(kp, std_yaml_val)

    def normalize(self, keypath: MULTI_KEYPATH_TYPE = None) -> None:
        for _, val, _ in self._iter_keypath(keypath):
            if isinstance(val, list):
                for elt in val:
                    self._normalize_me(elt)
            else:
                self._normalize_me(val)

    def _normalize_me(self, data: object) -> None:
        if hasattr(data, 'normalize'):
            data.normalize()

    def postprod(self, keypath: MULTI_KEYPATH_TYPE = None, tolerent: bool = True) -> benedict:
        results_captured = benedict()
        for kp, val, parser_module in self._iter_keypath(keypath):
            if not self._main_parsers[kp][TAG_USE_POST]:
                if not tolerent:
                    self._checker.raise_kpse_error(
                        _exception=KeyPathError,
                        fmt_str=f'No post-processing for {keypath!r}.',
                    )
                continue

            _, amdata_use = self._main_parsers[kp][TAG_AMDATA_USE]
            try:
                if amdata_use:
                    result = parser_module.postprod(amdata=self, data=val)
                else:
                    result = parser_module.postprod(val)
            except Exception as e:
                self._checker.raise_kpse_error(
                    _exception=PostProcessingError,
                    fmt_str=f'Post processing of {keypath!r}',
                    _sub_exception=e,
                )

            if result is not None:
                for tag in result:
                    if tag in results_captured:
                        self._checker.raise_kpse_error(
                            _exception=CriticalImplementationError,
                            fmt_str=f'Post processing tag {tag!r} has been used twice. Found with data {keypath!r}.',
                            tag=tag
                        )
                results_captured |= result

        return results_captured


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    TEST_WANTED = [1, 2]
    from pprint import pprint
    projdir = Path(__file__).parent

    while projdir.name != 'for-dev':
        projdir = projdir.parent

    if 1 in TEST_WANTED:
        mydir = projdir / 'aboutmeta'
        amdata = AMData.new_instance(flavour=TAG_IT_PROJECT, parent=mydir)
        amdata.build()
        amdata.standardize()
        amdata.normalize()
        amdata.postprod()

    if 2 in TEST_WANTED:
        mydir = projdir / 'aboutmeta' / 'contribute' / 'api' / 'parser' / 'readme'
        amdata = AMData.new_instance(flavour=TAG_ATOC, parent=mydir)
        amdata.build()
        results = amdata.postprod()
        for k, v in results.items():
            pprint(v)
