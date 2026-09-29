#!/usr/bin/env python3

from aboutmeta.core.log_conf import *

from dataclasses import dataclass
from pathlib     import Path


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

class DataPB:
    def __init__(
        self,
        dataname: str,
    ):
        self.dataname = dataname

###
# XXXX
###
    def msg(
        self,
        text: str,
    ):
        logging.info(text)

###
# XXXX
###
    def what(
        self,
        text: str,
    ):
        logging.info(text)

###
# XXXX
###
    def success(self):
        logging.info("OK")

###
# XXXX
###
    def pb(
        self,
        text: str,
    ):
        logging.warning(text)

###
# XXXX
###
    def failure(
        self,
        text: str,
    ):
        logging.critical(text)

###
# XXXX
###
    def exception(
        self,
        text: str,
    ):
        logging.error(text)


# ---------------------------- #
# -- DATA MANAGER INTERFACE -- #
# ---------------------------- #

###
# prototype::
#     yaml_val : this attribute will be used to store a "standard"
#                version of the data in the path::''about.yaml''
#                file. This attribute is also used for basing
#                printing.
#     data_pb : XXXX
#     YYY : XXXX
###
class DataManager:
    yaml_val: str
    data_pb : DataPB

###
# We make the class instance immutable and initiate its DataPB
# instance.
###
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls.data_pb = DataPB(cls.__name__)

        dataclass(frozen=True)(cls)

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
        foo: None

# GOOD
    print("----------")
    print("GOOD CASES")
    print("----------")

    mydata = MyData(foo = 'OK')

    print(mydata.foo)

    mydata.data_pb.what("what")
    mydata.data_pb.msg("msg")
    mydata.data_pb.success()
    mydata.data_pb.failure("failure")
    mydata.data_pb.exception("exception")

# BAD
    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    mydata.foo = "KO"
