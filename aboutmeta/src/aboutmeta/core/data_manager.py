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

    mydata.data_pb.what("What I test")
    mydata.data_pb.msg("My personal info")
    mydata.data_pb.success()

    mydata.data_pb.failure("Validation done has failed")
    mydata.data_pb.pb("My problem")

    try:
        1/0

    except Exception as e:
        mydata.data_pb.exception(e)

# BAD
    print()
    print("---------")
    print("BAD CASES")
    print("---------")

    mydata.foo = "KO"
