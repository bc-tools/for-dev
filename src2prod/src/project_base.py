#!/usr/bin/env python3

###
# This module provides the tools used to implement the monitoring of
# projects.
###


from typing import Union, List

from shutil     import copyfile
from subprocess import run
from yaml       import safe_load as yaml_load

from spkpb import (
    FORLOG,
    GLOBAL_STYLE_COLOR,
    VAR_TITLE,
    VAR_STEP_INFO,
    BaseCom,
    Path,
    Problems,
    Speaker,
)


# ------------------------------------------ #
# -- ABSTRACT CLASS FOR LOW LEVEL ACTIONS -- #
# ------------------------------------------ #

###
# This class implements basic technical methods which will be used by
# the ''project.Project'' class.
###
class ProjectBase(BaseCom):
    DIR_TAG  = 'dir'
    FILE_TAG = 'file'

###
# prototype::
#     project : the project folder.
#     erase   : ''True'' value allows to remove a none empty existing
#               target folder, whereas ''False'' doesn't.
###
    def __init__(
        self,
        project: Path,
        erase  : bool = False,
    ) -> None:
# User's choices.
        self.project: Path = project
        self.erase  : bool = erase

# To communicate.
        self.logfile: Path = project / f'{project.name}.src2prod.log'

        super().__init__(
            Problems(
                Speaker(
                    logfile = self.logfile,
                    style   = GLOBAL_STYLE_COLOR,
                )
            )
        )


















###
# prototype::
#     kind : the making kind
#
#     :action: this method resets everything.
#
#     :see: spkpb.problems.Problems.reset
###
    def reset_basecom(
        self,
        kind: str = 'SRC --> FINAL PRODUCT'
    ) -> None:
        super().reset()

        self.recipe(
            FORLOG,
                {VAR_TITLE:
                    f'"{self.project.name}": {kind}'},
        )

# Extra attributs.
        self.success         = True
        self.lof: List[Path] = []


###
# prototype::
#     :return: ???
###
    @property
    def project(self):
        return self._project


###
# prototype::
#     value :
#
#     :action: ???
###
    @project.setter
    def project(self, value: Path):
        if not isinstance(value, Path):
            raise TypeError("`project` must be a `Path` value")

        if not value.is_dir():
            raise IOError("`project` is not an existing folder")

        self._project = value


###
# prototype::
#     :acton: ????
###
    def yaml2config(self) -> None:
        TODO


###
# prototype::
#     :action: this method builds ''self.ignore_rules'' which is a dictionary.
#
# Here is how the dictionary looks like.
#
# python::
#     {
#         self.DIR_TAG : [
#             rule_1_to_ignore_some_dirs,
#             rule_2_to_ignore_some_dirs,
#             ...
#         ],
#         self.FILE_TAG : [
#             rule_1_to_ignore_some_files,
#             rule_2_to_ignore_some_files,
#             ...
#         ],
#     }
###
    def _build_ignore(self) -> None:
# A file to read?
        if not isinstance(self.ignore, Path):
            ignorerules = self.ignore

        else:
            self.recipe(
                {VAR_STEP_INFO:
                    f'Ignore rules in the file:'
                     '\n'
                    f'"{self.ignore}"'},
            )

            if not self.ignore.is_file():
                self.new_error(
                    what = self.ignore,
                    info = f'file with ignore rules not found.',
                )

                self.ignore_rules = None
                return

            with self.ignore.open(
                encoding = 'utf-8',
                mode     = 'r',
            ) as f:
                ignorerules = f.read()

# Let's build our internal dictionary.
        self.ignore_rules = {
            self.DIR_TAG : [],
            self.FILE_TAG: [],
        }

        for rule in ignorerules.split('\n'):
            if not(shortrule := rule.strip()):
                continue

# A dir rule.
            if shortrule.endswith('/'):
                context   = self.DIR_TAG
                shortrule = shortrule[:-1]

# A file rule.
            else:
                context = self.FILE_TAG

            self.ignore_rules[context].append(shortrule)








###
# prototype::
#     onedir : a dir to analyze.
#
#     :yield: the files in the folder ''onedir'' kept after the application
#             of the ignore rules.
#
# note::
#     \git is not used here.
###
    def iterfiles(self, onedir: Path) -> Path:
        for fileordir in onedir.iterdir():
            if fileordir.is_dir():
                if self.keepthis(
                    fileordir = fileordir,
                    kind      = self.DIR_TAG
                ):
                    for onefile in self.iterfiles(onedir = fileordir):
                        yield onefile

            elif self.keepthis(
                fileordir = fileordir,
                kind      = self.FILE_TAG
            ):
                yield fileordir


###
# prototype::
#     fileordir : the path of a file or a dir.
#     kind      : the kind of \io object.
#               @ kind in [self.DIR_TAG, self.FILE_TAG]
#
#     :return: ''True'' if the \io object must be kept regarding the ignore
#              rules, and ''False'' otherwise.
#
# note::
#     \git is not used here.
###
    def keepthis(
        self,
        fileordir: Path,
        kind     : str
    ) -> bool:
        for onerule in self.ignore_rules[kind]:
            if fileordir.match(onerule):
                return False

        return True


###
# prototype::
#     onedir : a dir.
#
#     :return: ''True'' if the folder doesn't exist yet or is empty and
#              ''False'' otherwise.
###
    def isempty(self, onedir: Path) -> bool:
# The folder doesn't exist.
        if not onedir.is_dir():
            return True

# Does the folder contain something?
        nothingfound = True

        for _ in onedir.iterdir():
            nothingfound = False
            break

# The job has been done.
        return nothingfound


###
# prototype::
#     src  : the path of the src file to copy.
#     dest : the path of the dest file that will be the copy.
#
#     :action: this method copies one file.
###
    def copyfile(
        self,
        src: Path,
        dest: Path,
    ) -> None:
        dest.parent.mkdir(
            parents  = True,
            exist_ok = True
        )

        copyfile(src, dest)


###
# prototype::
#     options : a list of options.
#
#     :return: the stripped standard output sent by the command.
#
# This method launches the command terminal::''git'' with the options given
# in the list ''options''.
###
    def rungit(self, options: List[str]) -> str:
        cmd = ['git'] + options

# Launch the command in the project folder.
        try:
            output = run(
                cmd,
                capture_output = True,
                cwd            = self.project
            )

# Can't launch the command.
        except FileNotFoundError as e:
            cmd = " ".join(cmd)

            self.new_error(
                what = self.src,
                info = f'can\'t use "{cmd}".',
            )
            return

# Command launched throws an error.
        if output.stderr:
            self.new_error(
                what = self.src,
                info = (
                    f'error throwed by "{cmd}":'
                     '\n'
                    f'"{self.decode(output.stderr)}".'
                ),
            )
            return

# The work has been done correctly.
        return self.decode(output.stdout).strip()



###
# prototype::
#     bytedatas : a byte content.
#
#     :return: the string obtained by decoding with the \utf8 encoding.
###
    def decode(self, bytedatas: bytes) -> str:
        return bytedatas.decode('utf-8')
