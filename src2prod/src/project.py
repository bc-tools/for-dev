#! /usr/bin/env python3

###
# This module implements all the logic needed to manage one project.
###


from shutil import rmtree

from multimd import Builder as MMDBuilder
from spkpb import *

from .project_base import *


# ------------------------ #
# -- PROJECT MANAGEMENT -- #
# ------------------------ #

###
# This class is the main one to use such as to easily manage a project
# following the "src-to-final-product" workflow.
###
class Project(ProjectBase):
    MD_SUFFIX = '.md'

###
# prototype::
#     opensession  : ''True'' is to reset eveything and open the communication
#                    and ''False'' starts directly the work.
#     closesession : ''True'' is to close the communication and
#                    ''False'' otherwise.
#     erase        : ''True'' asks to remove a none empty dest folder
#                    contrary to ''True''.
#
#     :action: this method builds the final product from the \src code.
#
# note::
#     The argument ''erase'' is here to leave the responsability of
#     removing a none empty folder to the user (my lawyers forced me
#     to add this feature).
###
    def build(
        self,
        opensession : bool = True,
        closesession: bool = True,
        erase       : bool = False
    ) -> None:
# Do we open the session?
        if opensession:
            self._start_one_session(
                title       = f'"{self.project.name}": UPDATE',
                timer_title = 'update'
            )

# Build the l.o.f.
        self.check(
            opensession  = False,
            closesession = False,
        )

        if not self.success:
            self._close_one_session(timer_title = 'update')
            return

# Safe mode?
        if (
            not erase
            and
            not self.isempty(self.dest)
        ):
            self.new_error(
                what = self.dest,
                info = (
                    'dest folder exists and is not empty '
                    '(safe mode used).'
                )
            )

            self._close_one_session(timer_title = 'update')

            return

# We can update the dest folder.
        for name in [
            'empty_dest',
            'copy_src2dest',
            'build_readme',
        ]:
            getattr(self, name)()

# Every copies has been made.
        self.recipe(
            {VAR_STEP_INFO:
                f'Dest folder updated.'}
        )

# Do we clode the session?
        if closesession:
            self._close_one_session(timer_title = 'update')


###
# prototype::
#     :action: this method creates or empties the dest folder.
###
    def empty_dest(self) -> None:
# The dest folder must be deletted.
        if self.dest.is_dir():
            action = 'emptied'

            rmtree(self.dest)

        else:
            action = 'created'

# Create a new version of the dest folder.
        self.dest.mkdir()

# We are so happy to talk about our exploit...
        self.recipe(
            {VAR_STEP_INFO:
                f'Dest folder has been {action}:'
                 '\n'
                f'"{self.dest}".'},
        )


###
# prototype::
#     :action: this method copies the files kept from the src
#              to the dest.
###
    def copy_src2dest(self) -> None:
# Indicating the start of the copying.
        nb_files = len(self.lof)
        plurial  = '' if nb_files == 1 else 's'

        self.recipe(
            {VAR_STEP_INFO:
                f'Copying {nb_files} file{plurial} from src to dest.'}
        )

# Let's copy each files.
        for srcfile in self.lof:
            destfile = self.dest / srcfile.relative_to(self.src)

            self.copyfile(
                src = srcfile,
                dest = destfile
            )


###
# prototype::
#     :action: this method writes the content into the final
#              path::''README'' file.
###
    def build_readme(self) -> None:
# No README to copy.
        if self.readme_src is None:
            return

# A folder with `MD` chuncks or a single file?
        if self._readme_is_file:
            readme_src = self.readme_src

        else:
            readme_src = self.project / 'README.md'

# Let ''multimd.buil.Builder'' does all the thankless job...
            MMDBuilder(
                src   = self.readme_src,
                dest  = readme_src,
                erase = self.erase,
            ).build()

# Now we just have a file to copy.
        self.copyfile(
            src = readme_src,
            dest = self._readme_dest
        )

# Let's talk...
        readme_rel = readme_src.relative_to(self.project)

        self.recipe(
            {VAR_STEP_INFO:
                f'"{readme_rel}" added to the dest.'}
        )


###
# prototype::
#     opensession  : ''True'' is to reset eveything and open the communication
#                    and ''False'' starts directly the work.
#     closesession : ''True'' is to close the communication and
#                    ''False'' otherwise.
#
#     :action: this method is the great bandleader building the list of files
#              to be copied to the dest dir.
###
    def check(
        self,
        opensession : bool = True,
        closesession: bool = True,
    ) -> None:
# Do we open the session?
        if opensession:
            self._start_one_session(
                title       = f'"{self.project.name}": LIST OF FILES',
                timer_title = 'build'
            )

# List of methods called.
        methodenames = [
            'check_readme',
            'build_ignore',
        ]

        if self.usegit:
            methodenames.append('check_git')

        methodenames.append('files_without_git')

        if self.usegit:
            methodenames.append('removed_by_git')

# Let's work.
        for name in methodenames:
            getattr(self, name)()

            if not self.success:
                break

# Do we close the session?
        if closesession:
            self._close_one_session(timer_title = 'build')


###
# prototype::
#     :action: this method checks the existence of a path::''README'' file
#              if the user has given such one, or a path::''readme'' folder.
###
    def check_readme(self) -> None:
# No external README.
        if self.readme_src is None:
            return

# Do we have an external README file?
        if self.readme_src.suffix:
            if not self.readme_src.is_file():
                self.new_error(
                    what  = self.readme_src,
                    info  = '"README" file not found.',
                    level = 1
                )
                return

            self._readme_is_file = True

# Do we have an external readme dir?
        else:
            if not self.readme_src.is_dir():
                self.new_error(
                    what  = self.readme_src,
                    info  = '"readme" folder not found.',
                    level = 1
                )
                return

            self._readme_is_file = False

# Let's talk...
        kind = '"README" file' if self._readme_is_file else '"readme" dir'

        self.recipe(
            {VAR_STEP_INFO:
                f'External {kind} to use:'
                 '\n'
                 f'"{self.readme_src}".'}
        )


###
# prototype::
#     :action: this method checks that \git can be used,
#              finds the branch on which we are working,
#              and verifies that there isn't any uncommitted changes in
#              the \src files.
#
# warning::
#     We do not want any uncommitted changes even on the ignored files because this
#     could imply some changes in the final product.
###
    def check_git(self) -> None:
        self.recipe(
            {VAR_STEP_INFO: f'Checking "git".'}
        )

# Let's go
        infos = {}

        for kind, options in [
# Current branch.
            ('branch', ['branch']),
# We don't want uncommitted files in our src folder!
            ('uncommitted', ['a']),
        ]:
            infos[kind] = self.rungit(options)

            if not self.success:
                return

# Branch used.
        for onebranch in infos['branch'].split('\n'):
            if onebranch.startswith('*'):
                branch = onebranch[1:].strip()
                break

        self.recipe(
            {VAR_STEP_INFO: f'Working in the branch "{branch}".'}
        )

# Uncommitted changes in our src?
        tosearch = f'{self.project.name}/{self.src.name}/'

        if (
            "Changes to be committed" in infos['uncommitted']
            and
            tosearch in infos['uncommitted']
        ):
            gitinfos = [
                x.strip()
                for x in infos['uncommitted'].split('\n')
                if tosearch in x
            ]

            nb_changes = len(gitinfos)
            howmany    = 'one' if nb_changes == 1 else 'several'
            plurial    = ''    if nb_changes == 1 else 's'

            if len(gitinfos) <= 5:
                whichuncommitted = ''

            else:
                whichuncommitted = ' the 5 first ones'
                gitinfos         = gitinfos[:5] + ['...']

            fictive_tab = '\n    + '
            gitinfos    = fictive_tab.join(gitinfos)

            self.new_error(
                what = self.src,
                info = (
                    f'{howmany} uncommitted file{plurial} found in the src folder. '
                    f'See{whichuncommitted} below.'
                    f'{fictive_tab}{gitinfos}'
                ),
                level = 1
            )
            return


###
# prototype::
#     :action: this method builds the list of files to keep just by using
#              the ignore rules.
#
# note::
#     \git is not used here.
###
    def files_without_git(self) -> None:
# Let's talk.
        self.recipe(
            {VAR_STEP_INFO:
                 'Starting the analysis of the src folder:'
                 '\n'
                f'"{self.src}".'},
        )

# Does the src dir exist?
        if not self.src.is_dir():
            self.new_error(
                what = self.src,
                info = 'src folder not found.',
            )
            return

# List all the files.
        self.lof = [
            f for f in self.iterfiles(self.src)
        ]

# An empty list stops the process.
        if not self.lof:
            self.new_critical(
                what = self.src,
                info = 'empty src folder.',
            )
            return

# Let's be proud of our 1st list.
        if self.usegit:
            whatused = 'the rules from "ignore"'

        else:
            whatused = 'only the rules from "ignore"'

            self._indicating_lof_found(
                output   = FORLOG,
                whatused = whatused
            )

        self._indicating_lof_found(
            output   = FORTERM,
            whatused = whatused
        )


###
# prototype::
#     :action: this method shrinks the list of files by using the ignore
#              rules used by \git.
#
# note::
#     The method ''rungit'' fails with ''options = ['check-ignore', '**/*'])'',
#     so we must test directly each path.
###
    def removed_by_git(self) -> None:
        len_lof_before = len(self.lof)

# Let's talk.
        self.recipe(
            FORTERM,
                {VAR_STEP_INFO:
                    'Removing unwanted files using "git".'},
        )

        self.lof = [
            onefile
            for onefile in self.lof
            if not self.rungit(
                options = [
                    'check-ignore',
                    onefile.relative_to(self.project)
                ]
            )
        ]

# Let's be proud of our 2nd list.
        len_lof = len(self.lof)

        if len_lof_before == len_lof:
            extra = ' No new file ignored.'

        else:
            nb_new_ignored = len_lof_before - len_lof
            plurial        = '' if nb_new_ignored == 1 else 's'

            extra = (
                f' {nb_new_ignored} new file{plurial} '
                 'ignored thanks to "git".'
            )

        self._indicating_lof_found(
            output   = FORTERM,
            whatused = '"git"',
            extra    = extra
        )

        self._indicating_lof_found(
            output   = FORLOG,
            whatused = '"git" and the rules from "ignore"',
        )


###
# prototype::
#     output   : the output(s) where we want to communicate.
#              @ :in: [FORTERM, FORLOG, FORALL]
#     whatused : the method used to shrink the list of files.
#     extra    : a small extra text.
#
# note::
#     This method is just a factorization.
###
    def _indicating_lof_found(
        self,
        output  : str,
        whatused: str,
        extra   : str = ''
    ) -> None:
        len_lof = len(self.lof)
        plurial = '' if len_lof == 1 else 's'

        self.recipe(
            output,
                {VAR_STEP_INFO:
                    f'{len_lof} file{plurial} found using {whatused}.{extra}'},
        )


###
# prototype::
#     title       : the title of the session.
#     timer_title : the title for the time stamp.
#
# note::
#     This method is just a factorization.
###
    def _start_one_session(
        self,
        title      : str,
        timer_title: str
    ) -> None:
        self.reset_speaker()

        self.timestamp(f'{timer_title} - start')

        self.recipe(
                {VAR_TITLE: title},
            FORTERM,
                {VAR_STEP_INFO:
                     'The log file used will be :'
                     '\n'
                    f'"{self.logfile}".'},
        )


###
# prototype::
#     timer_title : the title for the time stamp.
#
# note::
#     This method is just a factorization.
###
    def _close_one_session(
        self,
        timer_title: str
    ) -> None:
        self.resume()

        self.recipe(
            FORLOG,
                NL
        )

        self.timestamp(f'{timer_title} - end')
