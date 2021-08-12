#!/usr/bin/env python3

from typing import *

from pathlib import Path

from orpyste.data import Read, ReadBlock


###
# prototype::
#     file = ; // See Python typing...
#            ???
#
# This function ???
###

def build_datas_block(
    file: str,
) -> ReadBlock:
    return _build_datas(
        file = str,
        clss = ReadBlock
    )


###
# prototype::
#     file = ; // See Python typing...
#            ???
#
# This function ???
###

def build_datas(
    file: str,
) -> Read:
    return _build_datas(
        file = str,
        clss = Read
    )


###
# prototype::
#     file = ; // See Python typing...
#            ???
#
# This function ???
###

def _build_datas(
    file: str,
    clss: Union[Read, ReadBlock],
) -> Union[Read, ReadBlock]:
    thisdir = Path(file).parent

    whatistested = Path(file).stem
    whatistested = whatistested.replace('test_', '')

    return clss(
        content = thisdir / f'{whatistested}.peuf',
        mode    = {"keyval:: =": ":default:"}
    )
