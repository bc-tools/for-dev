#!/usr/bin/env python3

from collections import defaultdict
from yaml        import safe_load as yaml_load

from mistool.os_use import PPath as Path


# ! -- DEBUGGING -- ! #
# Clear the terminal.
# print("\033c", end="")
# ! -- DEBUGGING -- ! #


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = Path(__file__)
THIS_DIR  = Path(THIS_FILE).parent

PROJECT_DIR = THIS_DIR

while(PROJECT_DIR.name != 'CoFiUp'):
   PROJECT_DIR = PROJECT_DIR.parent


DOC_CONTENT_DIR = PROJECT_DIR / 'doc' / 'content'
TEST_DIR        = PROJECT_DIR / 'tests' / 'outputs'
TEST_EXA_DIR    = TEST_DIR / 'exadoc'

DEFAULT_CONFIG_NAME = "cfg.cfup.yaml"


# -------------- #
# -- SPEAKING -- #
# -------------- #

TAB_1 = ' '*4
TAB_2 = TAB_1*2
TAB_3 = TAB_1*3


# ------------------- #
# -- EXTRACT TESTS -- #
# ------------------- #

SUFFIXES = defaultdict(int)

def suffixit(onedir):
    return Path(
        f"{onedir}-{SUFFIXES[onedir]}"
    )


def testsfrom(pdir, testfiles):
    for pfile in pdir.glob('**/*.cfup.yaml'):
        testdir      = pfile.parent
        testdir_name = testdir.name

# Several config for the same data?
        if(
            testdir_name not in testfiles
            and
            testdir_name not in SUFFIXES
        ):
            dirtouse = testdir_name

        else:
            if testdir_name not in SUFFIXES:
                SUFFIXES[testdir_name] += 1

                renamed_dir = suffixit(testdir_name)

                if renamed_dir in testfiles:
                    raise Exception(
                        f"folder (re)name ''{renamed_dir}'' "
                        "already exists."
                    )

                testfiles[renamed_dir] = testfiles[testdir_name].copy()

                del testfiles[testdir_name]

            SUFFIXES[testdir_name] += 1
            dirtouse = suffixit(testdir_name)


        testfiles[dirtouse].append((
            pfile          ,  # Source
            pfile - testdir,  # Relative dest path
        ))

        for dpath in pfile.parent.glob('*'):
            if dpath.name.endswith('.cfup.yaml'):
                continue

            testfiles[dirtouse].append((
                dpath          ,  # Source
                dpath - testdir,  # Relative dest path
            ))


# ---------------------- #
# -- EXAMPLES TO TEST -- #
# ---------------------- #

print(f"{TAB_1}* Doc content - Looking for examples to test.")

testfiles = defaultdict(list)

for pdir in DOC_CONTENT_DIR.glob('**/examples/*'):
    if not pdir.is_dir():
        continue

    print(f"{TAB_2}+ {pdir - DOC_CONTENT_DIR}")

    testsfrom(pdir, testfiles)


# ---------------------- #
# -- COPYING EXAMPLES -- #
# ---------------------- #

print(f"{TAB_1}* Doc content - Copying examples to test.")

if TEST_EXA_DIR.is_dir():
    TEST_EXA_DIR.remove()


for destdir, paths in testfiles.items():
    for srcpath, reldetspath in paths:
# We normalize the name of the config file!
        if reldetspath.name.endswith('.cfup.yaml'):
            reldetspath = reldetspath.parent / DEFAULT_CONFIG_NAME

        destpath = destdir / reldetspath
        destpath = TEST_EXA_DIR / destpath

        srcpath.copy_to(destpath)
