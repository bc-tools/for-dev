#!/usr/bin/env python3

from functools import wraps

from aboutmeta.core.log_conf import *

from dataclasses import dataclass


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

###
# prototype::
#     dataname : XXXX
#
#
# LLLLL
###
def add_log_methods(*log_levels: list[str]) -> None:
    def decorator(cls):
        for one_log_level in log_levels:
            one_log_method = getattr(
                logging,
                one_log_level
            )

            def _make_logger(fn):
                @wraps(fn)
                def method(self, text: str):
                    message = self._with_prefix(text)

                    fn(message)

                return method

            setattr(
                cls,
                one_log_level,
                _make_logger(one_log_method)
            )

        return cls

    return decorator


###
# prototype::
#     dataname : XXXX
#
#
# LLLLL
###
@add_log_methods(
    "info",
    "warning",
    "critical",
    "error",
    "debug"
)
class DataPB:
    def __init__(
        self,
        dataname: str,
    ):
        self.dataname = dataname

###
# prototype::
#     data_inst : XXXX
#
#     :action: XXXX
###
    def start(
        self,
        data_inst: object,
    ):
        data_inst._errors_found = []

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def what(
        self,
        what: str,
    ):
        self.__what = what

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def _with_prefix(
        self,
        text: str,
    ):
        return f"[{self.dataname} - {self.__what}] {text}"

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def new_error(
        self,
        data_inst: object,
        data_attr: object,
        error_msg: str,
    ):
        msg = f"'{data_attr}': {error_msg}"

        self.error(msg)
        data_inst._errors_found.append(msg)

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def new_exception(
        self,
        data_inst : object,
        data_attr : object,
        _exception: str,
    ):
        msg = f"'{data_attr}': {_exception}"

        self.error(f"Exception catched\n{msg}")
        data_inst._errors_found.append(msg)

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def checking(
        self,
        data     : object
    ):
        self.info(f"Checking '{data}'")

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def no_checking(self):
        self.info("Nothing to check.")

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def _conclusion(
        self,
        validated: bool,
        data     : object
    ):
        if validated:
            status = "OK"
            desc   = "validated"

        else:
            status = "KO"
            desc   = "rejected"

        self.info(f"{status}\n'{data}' {desc}.")

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def rejected(
        self,
        data: object
    ):
        self._conclusion(
            validated = False,
            data      = data
        )

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def validated(
        self,
        data: object
    ):
        self._conclusion(
            validated = True,
            data      = data
        )


# ---------------------------- #
# -- DATA MANAGER INTERFACE -- #
# ---------------------------- #

###
# prototype::
#     yaml_val : this attribute will be used to store a "standard"
#                version of the data in the path::''about.yaml''
#                file. This attribute is also used for basing
#                printing.
#     data_pb  : XXXX class MyData(DataManager) --> attribute data_pb is equal to DataPB('MyData')
###
class DataManager:

###
# XXXX
###
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
###
# We make the class instance immutable and initiate its DataPB
# instance.
###
    def __init_subclass__(cls, **kwargs):
        cls.data_pb = DataPB(cls.__name__)

        dataclass()(cls)

###
# The magic method ''__str__'' should just display the string
# attribute ''yaml_val''.
###
    def __str__(self) -> str:
        return self.yaml_val


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
    from pprint import pprint

    setup_logging()

    class MyData(DataManager):
        yaml_val: str
        foo     : str

    mydata = MyData(
        yaml_val = '> OK',
        foo      = 'OK',
    )

    print(repr(mydata))

    mydata.data_pb.start(mydata)

    mydata.data_pb.what("What I test")
    mydata.data_pb.info("My personal info")
    mydata.data_pb.critical("Validation done has failed")
    mydata.data_pb.error("My problem")

    try:
        1/0

    except Exception as e:
        mydata.data_pb.new_exception(
            data_inst  = mydata,
            data_attr  = 'foo',
            _exception = e,
        )

    pprint(mydata._errors_found)
