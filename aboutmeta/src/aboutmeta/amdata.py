#!/usr/bin/env python3


# extract en mode cool : on veut juste un dict avec els cles des blocs et d'autres en plus ok
# extract(soft=False) pour mode strict

# postprod() : pour tous ces qu'i peut l'etre : résultat stocké dans un dict dédié

# posprod(keypath) : pour un sous jeu de donné ou une donné


from aboutmeta.specs.flavour.__ALL_FLAVOURS__ import *


class AMData:
    @classmethod
    def new_instance(cls, **kwargs):
        return cls(**kwargs)

    def __init__(self, x, y =5):
        self.x = x


test = AMData.new_instance(x = 3)

print(type(test))
