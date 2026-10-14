#!/usr/bin/env python3

import re

from dataclasses import field

from aboutmeta.core.data_manager import DataManager
from aboutmeta.core.errors       import ParsingError


# ------------------ #
# -- DATA MANAGER -- #
# ------------------ #

_PATTERN_ACRONYM_METADATA = re.compile(
    r'\[\s*(.*?)(?:\s*::\s*(.*?))?\s*\]|([^\[]+)'
)


###
# prototype::
#     spec  : YYYY
#     short : YYYY
#     desc  : YYYY
#
#
# note::
#     The ''short'' and ''desc'' attributes are build from the
#     value of the ''spec'' attribute.
###
class Acronym(DataManager):
    spec : str
    short: str = field(init = False)
    desc : str = field(init = False)

###
# prototype::
#     :action: derive the ''short'' and ''desc'' attributes from
#              ''self.spec''.
###
    def __post_init__(self):
        self.spec = self.spec.strip()

# Good use of the square brackets?
        bracket_is_opened = False

        for i, c in enumerate(self.spec):
            if c == '[':
                if bracket_is_opened:
                    raise ParsingError('KO 1')

                else:
                    bracket_is_opened = True

            elif c == ']':
                if not bracket_is_opened:
                    raise ParsingError('KO 2')

                else:
                    bracket_is_opened = False

        if bracket_is_opened:
            raise ParsingError('KO 3')

# Extract the spec parts.
        spec_parts = []

        for match in _PATTERN_ACRONYM_METADATA.finditer(self.spec):
            spec_initial, spec_final, other = match.groups()

            if not spec_initial is None:
                spec_initial = spec_initial.strip()

                if spec_final is None:
                    spec_final = spec_initial

                else:
                    spec_final = spec_final.strip()

                spec_parts.append((spec_initial, spec_final))

            elif not other is None:
                spec_parts.append((other, None))

# Build the short version.
        self.short = ''.join([
            p[1]
            for p in spec_parts
            if not p[1] is None
        ])

        if not self.short:
            raise ParsingError('No acronym found.')

# Build the raw description.
        self.desc = ''.join([
            p[0]
            for p in spec_parts
        ])

# Build the standard spec definition.
        self.spec = ''

        for p in spec_parts:
            if p[1] is None:
                self.spec += p[0]

            else:
                if p[0] == p[1]:
                    spec = p[0]

                else:
                    spec = '::'.join(p)

                self.spec += f'[{spec}]'


# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# GOOD
    print("\n------------\n")

    print("-- GOOD CASES --")

    for spec in [
        "   [about] [meta]data  ",
        "[about::@-]   [meta   ::   met-@]data",
    ]:
        mydata = Acronym(spec = spec)

        print()
        print(f"{spec   = }")
        print(f"{mydata = }")

# BAD
    # exit()

    print("\n------------\n")

    print("-- BAD CASES --")

    for spec in [
        "about metadata",
        "[about [meta]data",
        "[about] meta]data",
        "[about metadata",
        "about meta]data",
    ]:
        print()
        print(f"{spec = }")

        try:
            Acronym(spec = spec)

        except Exception as e:
            print(type(e).__name__, ':', e)

            notes = getattr(e, "__notes__", [])

            for i, n in enumerate(notes, start = 1):
                print(f'[{i}]. {n}')
