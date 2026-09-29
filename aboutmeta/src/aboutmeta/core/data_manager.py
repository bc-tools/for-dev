#!/usr/bin/env python3

from dataclasses import dataclass


# -------------------------- #
# -- DATA PB COMMUNICATOR -- #
# -------------------------- #

class DataPB:
    def __init__(self, dataname):
        print(dataname)


# ---------------------------- #
# -- DATA MANAGER INTERFACE -- #
# ---------------------------- #

###
# prototype::
#     yaml_val : this attribute will be used to store a "standard"
#                version of the data in the path::''about.yaml''
#                file. This attribute is also used for basing
#                printing.
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
    class MyData(DataManager):
        foo: None

    mydata = MyData(foo = 'OK')

    print(mydata.foo)

    data_pb.what("what")
    data_pb.msg("msg")
    data_pb.success()
    data_pb.failure("failure")
    data_pb.exception("exception")

    mydata.foo = "KO"
