#!/usr/bin/env python3

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
    def _added_prefix(
        self,
        text: str,
    ):
        return f"[{self.dataname}] {text}"

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def msg(
        self,
        text: str,
    ):
        logging.info(text)

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
        self.msg(
            self._added_prefix(text)
        )

###
# prototype::
#     :action: XXXX
###
    def success(self):
        logging.info(
            self._added_prefix("Sucessfull process")
        )

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def failure(
        self,
        text: str,
    ):
        logging.critical(
            self._added_prefix(f"Process failure\n{text}")
        )

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
        logging.error(
            self._added_prefix(f"Exception catched\n{text}")
        )

###
# prototype::
#     text : XXXX
#
#     :action: XXXX
###
    def pb(
        self,
        text: str,
    ):
        logging.error(
            self._added_prefix(f"Problem found\n{text}")
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
    mydata.data_pb.msg("My personal info")
    mydata.data_pb.success()

    mydata.data_pb.failure("Validation done has failed")
    mydata.data_pb.pb("My problem")

    try:
        1/0

    except Exception as e:
        mydata.data_pb.exception(e)
