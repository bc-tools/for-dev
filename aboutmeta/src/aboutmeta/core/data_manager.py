#!/usr/bin/env python3

from functools import wraps

from dataclasses import dataclass

from aboutmeta.core.log_conf import *


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
#     :return: class decorator function used to inject logging
#              methods into a class.
###
def add_log_methods(*log_levels: str) -> callable:
###
# prototype::
#     cls : target class to be decorated.
#
#     :return: decorated class with injected ''logging'' methods
#              that automatically prepend a text prefix using
#              the ''cls._prefixed'' method.
###
    def decorator(cls: object) -> object:
        for one_log_level in log_levels:
            one_log_method = getattr(
                logging,
                one_log_level
            )

###
# prototype::
#     fn : underlying ''logging'' function to be wrapped.
#
#     :return: method wrapper that prefixes the ''logging''
#              message, using the ''cls._prefixed'' method,
#              and then executes the 'logging' call.
###
            def _make_logger(fn: callable) -> callable:
                @wraps(fn)
                def method(self, text: str) -> None:
                    message = self._prefixed(text)

                    fn(message)

                return method

# Let's add the new method.
            setattr(
                cls,
                one_log_level,
                _make_logger(one_log_method)
            )

        return cls

    return decorator


###
# prototype::
#     cls : class equal to the ''data_cls'' attribute which is
#           used to update ''data_cls._errors_found'', a list
#           of issues.
#
#     :action: :see: add_log_methods[return]
#
#     :see: self.new_error,
#           self.new_exception
###
@add_log_methods(
    'info',
    'warning',
    'critical',
    'error',
    'debug'
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
#     :action: set internal ''__what'' attribute to ''what''.
###
    def what(
        self,
        what: str,
    ):
        self.__what = what

###
# prototype::
#     text : message.
#
#     :return: prefixed ''text'' value indicating in brackets
#              the type of data being studied and the specific
#              element under analysis.
###
    def _prefixed(
        self,
        text: str,
    ):
        return f'[{self.data_cls.__name__} - {self.__what}] {text}'

###
# prototype::
#     data      : :see: self._error_printed_stored
#     error_msg : :see: self._error_printed_stored
#
#
#     :action: print and store a message made with ''data'' and
#              ''error_msg''.
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
#     _exception : exception instance caught by a validation or
#                  normalization process.
#
#     :action: print and store a text showing type and message
#              of the exception, and the problematic ''data''.
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
            prefix    = f'{type(_exception).__name__}: ',
            error_msg = str(_exception),
        )

###
# prototype::
#     data      : data.
#     error_msg : error message.
#     prefix    : optional prefix to add before ''error_msg''.
#
#     :action: print an error logging message and store it in
#              the attribute ''data_cls._errors_found''.
#              The message is made by added ''prefix'', if not
#              empty, and ''data'' before ''error_msg''.
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
#     :action: display one text stating that data is being
#              checked.
###
    def checking(
        self,
        data: object
    ):
        self.info(f"Checking '{data}'.")

###
# prototype::
#     :action: display one text stating that nothing needs to
#              be checked.
###
    def no_check(self):
        self.info('Nothing to check.')

###
# prototype::
#     data : data that has been rejected.
#
#     :action: display text indicating data rejection.
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
#     :action: display text indicating data validation.
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
#     is_validated : boolean indicating validation or rejection
#                    of the tested data.
#
#     :action: display text indicating rejection or validation
#              of the data.
###
    def _conclusion(
        self,
        data        : object,
        is_validated: bool,
    ):
        if is_validated:
            status, desc = 'OK', 'validated'

        else:
            status, desc = 'KO', 'rejected'

        self.info(f"{status}\n'{data}' {desc}.")


# ---------------------------- #
# -- DATA MANAGER INTERFACE -- #
# ---------------------------- #

###
# note::
#     All ''DataManager'' instances always have the ''data_pb''
#     \cls \attr that must be used for validation process
#     communications.
###
class DataManager:

###
# We initiate the ''data_pb'' attribute with the actual class,
# and make the class a subclass of ''dataclasses.dataclass''.
###
    def __init_subclass__(
        cls,
        **kwargs
    ):
        cls.data_pb = DataPB(cls)

        dataclass()(cls)


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
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

    print(f'{mydata!r}')

    print('---')

    data_pb.what('Test 1')
    data_pb.start()
    data_pb.checking('something good')
    data_pb.info('My personal info')
    data_pb.validated('something good')

    print('---')

    data_pb.what('Test 2')
    data_pb.start()
    data_pb.checking('something bad')
    data_pb.error('My problem')
    data_pb.critical('Validation done has failed')

    try:
        1/0

    except Exception as e:
        data_pb.new_exception(
            data       = 'mydivision',
            _exception = e,
        )

    data_pb.rejected('Houston')

    pprint(mydata._errors_found)

    print('---')

    data_pb.what('Test 3')
    data_pb.start()

    data_pb.no_check()

    pprint(mydata._errors_found)
