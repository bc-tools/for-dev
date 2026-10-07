#!/usr/bin/env python3

from functools import wraps

from aboutmeta.core.log_conf import *

from dataclasses import dataclass


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

###
# prototype::
#     log_levels : XXXX
#
#     :return:
#
#
# LLLLL
###
def add_log_methods(*log_levels: str) -> callable:
###
# prototype::
#     cls : XXXX
#
#     :return:
#
#
# LLLLL
###
    def decorator(cls: object) -> object:
        for one_log_level in log_levels:
            one_log_method = getattr(
                logging,
                one_log_level
            )

###
# prototype::
#     fn : XXXX
#
#     :return:
#
#
# LLLLL
###
            def _make_logger(fn: callable) -> callable:
                @wraps(fn)
                def method(self, text: str) -> None:
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
#     what : XXXX
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
#     :return: XXXX
###
    def _with_prefix(
        self,
        text: str,
    ):
        return f"[{self.dataname} - {self.__what}] {text}"

###
# prototype::
#     data_inst :
#     data_attr :
#     error_msg :
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
#     data_inst  :
#     data_attr  :
#     _exception :
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
#     data : data to check.
#
#     :action: displaying text that indicates data is being checked.
###
    def checking(
        self,
        data     : object
    ):
        self.info(f"Checking '{data}'")

###
# prototype::
#     :action: displaying text stating that nothing needs to be
#              checked.
###
    def no_check(self):
        self.info("Nothing to check.")

###
# prototype::
#     data : data that has been rejected.
#
#     :action: displaying text that indicates data rejection.
#
#     :see: self._conclusion
###
    def rejected(
        self,
        data: object
    ):
        self._conclusion(
            data         = data,
            is_validated = False,
        )

###
# prototype::
#     data : data that has been validated.
#
#     :action: displaying text that indicates data validation.
#
#     :see: self._conclusion
###
    def validated(
        self,
        data: object
    ):
        self._conclusion(
            data         = data,
            is_validated = True,
        )

###
# prototype::
#     data         : data that has been tested to be validated.
#     is_validated : boolean indicating the validation or rejection
#                    of the tested data.
#
#     :action: displaying text that indicates data rejection or
#              validation.
###
    def _conclusion(
        self,
        data        : object,
        is_validated: bool,
    ):
        if is_validated:
            status, desc = "OK", "validated"

        else:
            status, desc = "KO", "rejected"

        self.info(f"{status}\n'{data}' {desc}.")


# ---------------------------- #
# -- DATA MANAGER INTERFACE -- #
# ---------------------------- #

###
# note::
#     ''DataManager'' instances must have the following attributes.
#
#         1) The ''yaml_val'' attribute stores the user-input data
#         coming from an `about.yaml` file.
#
#         1) The ''data_pb'' attribute must be used for validation
#         process communications.
###
class DataManager:

###
# prototype::
#     :action: initializing all attributes according to subclass
#              specifications.
###
    def __init__(
        self,
        **kwargs
    ):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

###
# We initiate the ''data_pb'' attribute to use the subclass name,
# and make the class a subclass of ''dataclasses.dataclass''.
###
    def __init_subclass__(
        cls,
        **kwargs
    ):
        cls.data_pb = DataPB(cls.__name__)

        dataclass()(cls)

###
# The method ''__str__'' just displays the string ''yaml_val''
# attribute.
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
        yaml_val = '-> OK <-',
        foo      = 'OK',
    )

    data_pb = mydata.data_pb

    print(repr(mydata))

    data_pb.start(mydata)

    data_pb.what("Test 0")
    data_pb.no_check()

    data_pb.what("Test 1")
    data_pb.checking('something good')
    data_pb.info("My personal info")
    data_pb.validated('something good')

    data_pb.what("Test 2")
    data_pb.error("My problem")
    data_pb.critical("Validation done has failed")

    try:
        1/0

    except Exception as e:
        data_pb.new_exception(
            data_inst  = mydata,
            data_attr  = 'foo',
            _exception = e,
        )

    data_pb.rejected('something bad')

    pprint(mydata._errors_found)
