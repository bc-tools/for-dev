#!/usr/bin/env python3

from functools import wraps

from aboutmeta.core.log_conf import *

from dataclasses import dataclass


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

def log_methods(*levels: str):
    def decorator(cls):
        for level in levels:
            level_lower = level.lower()
            log_func = getattr(logging, level_lower, None)

            if not callable(log_func):
                continue

            def _make_logger(fn):
                @wraps(fn)
                def method(self, text: str):
                    message = self._with_prefix(text)
                    fn(message)
                return method

            setattr(cls, level_lower, _make_logger(log_func))
        return cls
    return decorator


###
# prototype::
#     dataname : XXXX
#
#
# LLLLL
###
@log_methods("info", "warning", "critical", "error", "debug")
class DataPB:
    def __init__(
        self,
        dataname: str,
    ):
        self.dataname = dataname


###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def what(
        self,
        text: str,
    ):
        self.__what = text

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
    def exception(
        self,
        text: str,
    ):
        self.error(f"Exception catched\n{text}")

    def checking(
        self,
        data     : object
    ):
        self.info(f"Checking '{data}'")


    def no_checking(self):
        self.info("Nothing to check.")



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


    def rejected(
        self,
        data: object
    ):
        self._conclusion(
            validated = False,
            data      = data
        )


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
    setup_logging()

    class MyData(DataManager):
        yaml_val: str
        foo     : str

    mydata = MyData(
        yaml_val = '> OK',
        foo      = 'OK',
    )

    print(repr(mydata))

    mydata.data_pb.what("What I test")
    mydata.data_pb.info("My personal info")
    mydata.data_pb.critical("Validation done has failed")
    mydata.data_pb.error("My problem")

    try:
        1/0

    except Exception as e:
        mydata.data_pb.exception(e)
