#!/usr/bin/env python3

from collections import defaultdict
from json        import dumps
import re

from semantic_version import Version

from mistool.os_use import PPath

# ! -- DEBUGGING -- ! #
# Clear the terminal.
print("\033c", end="")
# ! -- DEBUGGING -- ! #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SRC_DIR = PPath(__file__)

while SRC_DIR.name != "cbdevtools":
    SRC_DIR = SRC_DIR.parent

CHGES_DIR    = SRC_DIR / "changes"
VERSION_FILE = SRC_DIR / "VERSION.json"


# ----------- #
# -- TOOLS -- #
# ----------- #

PATTERN_TITLE = re.compile("\n==\n(\d+.*)\n==\n")

MEANING_VERSION_PARTS = ['major', 'minor', 'patch', 'prerelease']
MEANING_DATE          = ['year', 'month', 'date']


def isbigger(version_1, version_2):
    for m in MEANING_VERSION_PARTS:
        if version_1[m] > version_2[m]:
            return True

        elif version_1[m] < version_2[m]:
            return False

        if m == 'prerelease':
            raise Exception(
                 'no support of comparisons based on '
                 '"prerelease part " for the moment.'
                f'\n{version_1 = }'
                f'\n{version_2 = }'
            )


# ---------------------- #
# -- CHANGE LOG FILES -- #
# ---------------------- #

print(f"   * Looking for the version NB. in the change log.")

versions_found = defaultdict(list)

chge_files = [
    f
    for f in CHGES_DIR.walk('file::**')
    if(f.stem.isdigit())
]

chge_files.sort()
chge_files.reverse()

nb_versions_found = {}

for path in chge_files:
    with path.open(
        encoding = 'utf-8',
        mode     = 'r',
    ) as f:
        content = f.read()

    year  = path.parent.name
    month = path.stem

    titles = re.findall(
        PATTERN_TITLE,
        content
    )

    if titles is None:
        continue

    for t in titles:
        t = t.strip()

        allnbsversion = (
            f'See the title ''{t}'' in the file '
            f'changes/{year}/{month}.txt'
        )

        if not '(' in t:
            continue

        assert t[-1] == ')', \
               (
                 'missing '')'' at the end.'
                 '\n' + allnbsversion
               )

        day, *version = t.split('(')

        assert len(version) == 1, \
               (
                 'invalid number of ''(''.'
                 '\n' + allnbsversion
               )

        version = version[0]
        version = version[:-1].strip()
        version = Version(version)


        day  = day.strip()
        date = (year, month, day)

# ! -- DEBUGGING -- ! #
        # print(f"{date = }")
# ! -- DEBUGGING -- ! #


        fullversion = str(version)

        assert not fullversion in nb_versions_found, \
               (
                 '{fullversion} already used.'
                 '\n' + allnbsversion +
                 '\nSee the most recent date '
                f'''{"-".join(nb_versions_found[fullversion])}''.'
               )

        nb_versions_found[fullversion] = date

        about = {
            m: version.__getattribute__(m)
            for m in MEANING_VERSION_PARTS
        }

        about['full'] = fullversion

        versions_found[date].append(about)


# ! -- DEBUGGING -- ! #
# from pprint import pprint
# pprint(versions_found)
# print()
# pprint(nb_versions_found)
# exit()
# ! -- DEBUGGING -- ! #


# --------------------- #
# -- LAST VERSION NB -- #
# --------------------- #

print(f"   * Update of the file ''VERSION.json''.")

if not versions_found:
    about_version = {}

else:
    for date, allnbsversion in versions_found.items():
        lastversion = None

        for oneversion in allnbsversion:
            if(
                lastversion is None
                or
                isbigger(oneversion, lastversion)
            ):
                lastversion = oneversion

        lastversion['date'] = {
            m: date[i]
            for i, m in enumerate(MEANING_DATE)
        }

        about_version = lastversion.copy()

        break


content = dumps(about_version)

with VERSION_FILE.open(
    encoding = "utf-8",
    mode     = "w",
) as f:
    f.write(content)


if about_version:
    what = "last"
    xtra = f": {about_version['full']}"

else:
    what = "no"
    xtra = ''

print(f"   * {what.title()} version NB. found{xtra}.")
