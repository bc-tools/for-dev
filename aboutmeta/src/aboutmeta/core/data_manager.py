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
#     cls : XXXX
#         @ ???? atttribut _errors_found obligé
#
#
# LLLLL   possibilité et réserver _errors_found
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
        cls: object,
    ):
        self.data_cls = cls

###
# prototype::
#     :action: setting the ''errors_found'' attribute of
#              ''self.data_cls'' to an empty list.
###
    def start(self):
       self.data_cls._errors_found = []

###
# prototype::
#     what : short text describing an ongoing process.
#
#     :action: setting internal ''__what'' attribute to ''what''.
###
    def what(
        self,
        what: str,
    ):
        self.__what = what

###
# prototype::
#     text : a message.
#
#     :return: prefixed ''text'' value indicating in brackets the
#              type of data being studied and the specific element
#              under analysis.
###
    def _with_prefix(
        self,
        text: str,
    ):
        return f"[{self.data_cls.__name__} - {self.__what}] {text}"

###
# prototype::
#     data      : XXXX
#     error_msg : an error message.
#
#     :action: XXXX
###
    def new_error(
        self,
        data     : object,
        error_msg: str,
    ):
        msg = f"'{data}': {error_msg}"

        self._error_printed_stored(
            msg_printed = msg,
            msg_stored  = msg,
        )

###
# prototype::
#     data       : :see: self.new_error
#     _exception : exception caught by a validation or normalization
#                  process.
#
#     :action: XXXX
###
    def new_exception(
        self,
        data      : object,
        _exception: str,
    ):
        msg = f"'{data}': {_exception}"

        self._error_printed_stored(
            msg_printed = f"Exception catched\n{msg}",
            msg_stored  = msg,
        )

###
# prototype::
#     msg_printed : an error logging message to be "printed".
#     msg_stored  : an error to be stored in the attribute
#                   ''data_cls._errors_found''.
#
#     :action: printing and storing error messages.
###
    def _error_printed_stored(
        self,
        msg_printed: str,
        msg_stored : str,
    ):
        self.error(msg_printed)

        self.data_cls._errors_found.append(msg_stored)

###
# prototype::
#     data : data to check.
#
#     :action: displaying text that indicates data is being checked.
###
    def checking(
        self,
        data: object
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
#     ''DataManager'' instances always have the following attributes.
#
#         1) The ''yaml_val'' attribute stores the user-input data
#         coming from an path::''about.yaml'' file.
#
#         1) The ''data_pb'' attribute must be used for validation
#         process communications.
###
class DataManager:

###
# We initiate the ''data_pb'' attribute with the actual class, and
# make the class a subclass of ''dataclasses.dataclass''.
###
    def __init_subclass__(
        cls,
        **kwargs
    ):
        cls.data_pb = DataPB(cls)

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

    data_pb.start()

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
            data       = 'mydivision',
            _exception = e,
        )

    data_pb.rejected('something bad')

    pprint(mydata._errors_found)


    data_pb.what("New data test")
    data_pb.start()
    data_pb.no_check()

    pprint(mydata._errors_found)
