#!/usr/bin/env python3

class Lang:
    def __init__(
        self,
        std,
        name,
        territory
    ):
        self.std       = std
        self.name      = name
        self.territory = territory

    def __str__(self):
        return self.std

    def __repr__(self):
        return f"""
aboutmeta.data.lang.Lang(std='{self.std}', name='{self.name}', territory='{self.territory}')
        """.strip()
