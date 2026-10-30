class AMData:
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
