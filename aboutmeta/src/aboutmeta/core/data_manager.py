#!/usr/bin/env python3

from functools import wraps

from aboutmeta.core.log_conf import *

from dataclasses import dataclass


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

###
# prototype::
#     log_levels : ''logging'' level names
#                @ log_levels in [
#                      'info',
#                      'warning',
#                      'critical',
#                      'error',
#                      'debug',
#                  ]
#
#     :return: a class decorator function used to inject logging
#              methods into a class.
###
def add_log_methods(*log_levels: str) -> callable:
###
# prototype::
#     cls : the target class to be decorated.
#
#     :return: the decorated class with injected ''logging'' methods
#              that automatically prepend a text prefix using the
#              ''cls._prefixed'' method.
###
    def decorator(cls: object) -> object:
        for one_log_level in log_levels:
            one_log_method = getattr(
                logging,
                one_log_level
            )

###
# prototype::
#     fn : the underlying ''logging'' function to be wrapped.
#
#     :return: a method wrapper that prefixes the ''logging'' message,
#              using the ''cls._prefixed'' method, and then executes
#              the 'logging' call.
###
            def _make_logger(fn: callable) -> callable:
                @wraps(fn)
                def method(self, text: str) -> None:
                    message = self._prefixed(text)

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
#     cls : this class is equal to the ''data_cls'' attribute which
#           is used to update ''data_cls._errors_found'', a list of
#           issues.
#
#     :see: self.new_error,
#           self.new_exception
#
#
# note::
#     The ''add_log_methods'' decorator defines methods that invoke
#     their corresponding ''logging'' ones, automatically prepending
#     a text (cf. ''self._prefixed'').
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
    def _prefixed(
        self,
        text: str,
    ):
        return f"[{self.data_cls.__name__} - {self.__what}] {text}"

###
# prototype::
#     data      : :see: self._error_printed_stored
#     error_msg : :see: self._error_printed_stored
#
#
#     :action: printing and storing a message made with ''error_msg''
#              and ''data''.
#
#     :see: self._error_printed_stored
###
    def new_error(
        self,
        data     : object,
        error_msg: str,
    ):
        self._error_printed_stored(
            data      = data,
            error_msg = error_msg,
        )

###
# prototype::
#     data       : :see: self._error_printed_stored
#     _exception : exception caught by a validation or normalization
#                  process.
#
#     :action: printing and storing a message indicated the exception,
#              its name and ''data''.
#
#     :see: self._error_printed_stored
###
    def new_exception(
        self,
        data      : object,
        _exception: Exception,
    ):
        self._error_printed_stored(
            data      = data,
            prefix    = f"{type(_exception).__name__}: ",
            error_msg = str(_exception),
        )

###
# prototype::
#     data      : a data.
#     error_msg : an error message.
#     prefix    : an optional prefix to add before ''error_msg''.
#
#     :action: printing an error logging message and storing it in the
#              attribute ''data_cls._errors_found''.
#              The message is made by added ''prefix'', if not empty,
#              and ''data'' before ''error_msg''.
###
    def _error_printed_stored(
        self,
        data     : object,
        error_msg: str,
        prefix   : str = '',
    ):
        msg = f"{prefix}'{data}': {error_msg}"

        self.error(msg)
        self.data_cls._errors_found.append(msg)

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

    print("\n------------\n")

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

    print("\n------------\n")

    data_pb.what("Test 1")
    data_pb.start()
    data_pb.checking('something good')
    data_pb.info("My personal info")
    data_pb.validated('something good')

    print("\n------------\n")

    data_pb.what("Test 2")
    data_pb.start()
    data_pb.checking('something bad')
    data_pb.error("My problem")
    data_pb.critical("Validation done has failed")

    try:
        1/0

    except Exception as e:
        data_pb.new_exception(
            data       = 'mydivision',
            _exception = e,
        )

    data_pb.rejected('Houston')

    pprint(mydata._errors_found)

    print("\n------------\n")

    data_pb.what("Test 3")
    data_pb.start()

    data_pb.no_check()

    pprint(mydata._errors_found)
