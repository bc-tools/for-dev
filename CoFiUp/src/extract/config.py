#!/usr/bin/env python3

from typing import Union


from pathlib import Path
import              yaml


class Config:
    def __init__(
        self,
        config: Union[dict, Path]
    ):
        ...
# with open(cfg_cfup, mode='r') as file:
#     yaml_data = yaml.load(file, Loader=yaml.BaseLoader)
