class AMData:
    def __recu_parse(
        self,
        data : dict,
        specs: dict
    ) -> dict:
        data_parsed = {}

# Illegal alternatives?
        self.__no_alt_keys_together(data, specs)

# Let's parse...
        for key, val in data.items():
# Legal key?
            if not key in specs:
                raise KeyError(f"unknown key ''{key}''.")

            loc_specs = specs[key]

# Good kind of data?
            key_type = loc_specs[TAG_SPECS_TYPE]

            needed = ""

            match key_type:
                case "BLOCK":
                    if not isinstance(val, dict):
                        needed = "block"

                case "DATA":
                    if loc_specs[TAG_SPECS_LIST_OF]:
                        if not isinstance(val, list):
                            needed = "list of data"

                    elif not isinstance(val, str):
                        needed = "data"

            if needed:
                raise ValueError(
                    f"content of ''{key}'' must be a {needed}."
                )

# Block data needs a recursive work.
            if key_type == TAG_SPECS_BLOCK:
                data_parsed[key] = self.__recu_parse(
                    val,
                    loc_specs[TAG_SPECS_CONTENT]
                )

# list of data needs an iterative parsing.
            else:
                data_parsed[key] = self.parse_val(
                    val           = val,
                    is_list_of    = loc_specs[TAG_SPECS_LIST_OF],
                    parser_name   = loc_specs[TAG_SPECS_PARSER],
                    use_post_prod = loc_specs[TAG_SPECS_POST_PROD],
                )

# Job done.
        return data_parsed

### TODO
# prototype::
###
    def parse_val(
        self,
        val            : str | list[str],
        is_list_of     : bool,
        parser_name    : str,
        use_post_prod  : bool,
        allow_post_prod: bool = True,\
    ) -> Any:
        if parser_name == TAG_PARSER_STR:
            _parser = str

        else:
            _parser = ALL_PARSERS[parser_name]

        if parser_name == TAG_PARSER_TOCPATH:
            parser = lambda x: _parser(
                self._yaml_file_dir,
                x
            )

        else:
            parser = lambda x: _parser(x)

        if is_list_of:
            for i, d in enumerate(val):
                val[i] = parser(val[i])

            if (allow_post_prod and use_post_prod):
                val = ALL_MAPPERS[parser_name](AMData, val)

            return val

        return parser(val)


###
# prototype::
#     data  : one piece of data (either a block, a list, or a final
#             data).
#     specs : "local" \specs corresponding to the data analyzed.
#
#     :action: verification that two competing keys are not used
#              simultaneously.
###
    def __no_alt_keys_together(
        self,
        data : dict,
        specs: dict
    ) -> None:
        if specs[TAG_SPECS_ALT_ALL]:
            keys_set   = set(data.keys())
            to_analyze = keys_set.intersection(
                set(specs[TAG_SPECS_ALT_ALL])
            )

            if len(to_analyze) > 1:
                for no_alt in specs[TAG_SPECS_ALT_TUPLES]:
                    common_keys = keys_set.intersection(no_alt)

                    if len(common_keys) > 1:
                        common_keys = list(common_keys)
                        common_keys.sort()
                        common_keys = [f"''{k}''" for k in common_keys]
                        common_keys = ', '.join(common_keys)

                        raise ValueError(
                            f"just use on the keys {common_keys}."
                        )

###
# prototype::
#     what      : either ''None'' to validate evrything, or a
#                 virtual path to a block or data to be validated.
#                 In the case of a block, a recursive search for
#                 the data to be validated is performed automatically.
#     erase_log : set to ''True'', this \arg allows to erase an
#                 existing ''LOG_FILE'' file used to store errors.
#     no_color  : :see: data.logconf.setup_logging
#
#     :return: the number of errors found.
#
#     :see: self.__recu_validate
#
#
# note::
#     The validation process is detailed in the terminal, but only
#     errors are recorded in the ''LOG_FILE'' file.
###
    def validate(
        self,
        what     : (str | None) = None,
        erase_log: bool = False,
        no_color : bool = False
    ) -> int:
        setup_logging(no_color)

        self.at_least_one_validation = False

# Which data to validate?
        if what is None:
            data = self.data

        else:
            data = self.data(what)

# Do we have to erase the log file?
        if erase_log:
            Path(LOG_FILE).touch()
            Path(LOG_FILE).write_text("")

# Let's delegate the work to a recursive company.
        return self.__recu_validate(data)

###
# prototype::
#     data : one piece of data (either a ''BoxPlus'', a list, or a
#            final data).
#
#     :return: the \nb of \pbs found during the validation of ''data''.
###
    def __recu_validate(
        self,
        data: Any
    ) -> int:
        nb_pbs = 0

# One dict?
        if isinstance(data, BoxPlus):
            for key, val in data.items():
                nb_pbs += self.__recu_validate(val)

# One list?
        elif isinstance(data, list):
            for val in data:
                nb_pbs += self.__recu_validate(val)

# One data to validate?
        elif hasattr(data, 'validate'):
            self.at_least_one_validation = True

            nb_pbs += data.validate()

        return nb_pbs
