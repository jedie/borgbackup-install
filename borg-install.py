#!/usr/bin/env python3

import cmd
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

APT_PACKAGES = (
    'python3 python3-dev python3-pip python3-venv libssl-dev'
    ' openssl libacl1-dev libacl1 build-essential libfuse-dev fuse pkg-config'
)

BORG_ENV_PATH = Path('/opt/borgbackup-env/')
VENV_PIP_PATH = BORG_ENV_PATH / 'bin' / 'pip3'
BORG_PYPI_NAME = 'borgbackup[fuse]'

BORG_VENV_PATH = BORG_ENV_PATH / 'bin' / 'borg'
BORG_DST_PATH = Path('/usr/local/bin/')


def verbose_check_call(*, info, command, verbose=True, quite=False, **kwargs):
    """
    'verbose' version of subprocess.check_call()
    """
    print()
    if not quite:
        print('_' * 100)
        if info:
            print(f' *** {info} ***', flush=True)

        if verbose:
            msg = f'call: {command!r}'
            verbose_kwargs = ', '.join(f'{k}={v!r}' for k, v in sorted(kwargs.items()))
            if verbose_kwargs:
                msg += f' (kwargs: {verbose_kwargs})'
            print(f'({msg})\n', flush=True)

    popenargs = shlex.split(command)
    subprocess.check_call(popenargs, universal_newlines=True, env=os.environ, **kwargs)
    sys.stdout.flush()


def symlink(file_path, destination):
    print('\n')
    print(f' *** Symlink "{file_path}" to "{destination}" ***')

    assert destination.is_dir(), f'Directory "{destination}" not found!'

    destination = Path(destination, file_path.name)
    if destination.is_file():
        # remove existing symlink to "refresh" it
        destination.unlink()

    destination.symlink_to(file_path)


class AbortCommand(Exception):
    pass


class BaseCmd(cmd.Cmd):
    intro = ''
    prompt = ''
    file = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        args = sys.argv[1:]
        if args:
            self.cmdqueue = [
                # shlex.join(args) # new in Python 3.8
                ' '.join(shlex.quote(arg) for arg in args)
            ]
        else:
            self.cmdqueue = ['help']  # Display the help on start

    def get_doc_line(self, command):
        """
        return the first line of the DocString.
        If no DocString: return None
        """
        assert command.startswith('do_')
        doc = getattr(self, command, None).__doc__ or ''
        doc = doc.strip().split('\n', 1)[0]
        return doc

    def do_help(self, arg):
        """
        List available commands with 'help' or detailed help with 'help command'.
        """
        if arg:
            # Help for one command
            return super().do_help(arg)

        print(self.doc_leader)
        print(self.doc_header)

        commands = sorted(name for name in self.get_names() if name.startswith('do_'))
        max_length = max(len(name) for name in commands) - 3
        for command in commands:
            doc_line = self.get_doc_line(command) or '(Undocumented command)'
            command = '{command:{width}}'.format(command=command[3:], width=max_length)  # remove 'do_' prefix
            print(f' {command} - {doc_line}')

    def do_quit(self, arg=None):
        """
        Exit this shell. (Or just hit Ctrl-C ;)
        """
        print('bye')
        return True  # exit shell

    def postcmd(self, stop, line):
        if len(sys.argv) > 1:
            # exit shell if we are called with commandline arguments
            stop = True
        return stop

    def cmdloop(self, *args, **kwargs):
        try:
            super().cmdloop(*args, **kwargs)
        except KeyboardInterrupt:
            self.do_quit()

    def onecmd(self, line):
        print()
        try:
            stop = super().onecmd(line)
        except AbortCommand as err:
            print(f'ERROR: {err}')
            stop = False  # Don't exist shell after a error
        print()
        return stop


###############################################################################################


class BorgInstallShell(BaseCmd):
    intro = 'Welcome to BordBackup install shell'
    prompt = '(borg-install) '

    def do_install(self, args=None):
        """
        install BorgBackup using virtualenv and pip
        """

        verbose_check_call(
            info='install the dependencies for Debian / Ubuntu',
            command=f'apt-get install {APT_PACKAGES}',
        )

        if BORG_ENV_PATH.is_dir():
            info = f'Recreate existing venv in "{BORG_ENV_PATH}"'
            command = f'python3 -m venv --clear {BORG_ENV_PATH}'
        else:
            info = f'Create venv in "{BORG_ENV_PATH}"'
            command = f'python3 -m venv {BORG_ENV_PATH}'

        verbose_check_call(info=info, command=command)

        self._update_venv_pip()

        verbose_check_call(
            info=f'Install "{BORG_PYPI_NAME}" via pip', command=f'{VENV_PIP_PATH} install {BORG_PYPI_NAME}'
        )

        self._update_symlinks()

    def do_update(self, args=None):
        """
        update BorgBackup installation
        """
        self._update_venv_pip()
        verbose_check_call(
            info=f'Update "{BORG_PYPI_NAME}" via pip', command=f'{VENV_PIP_PATH} install --upgrade {BORG_PYPI_NAME}'
        )
        self._update_symlinks()

    def do_uninstall(self, args=None):
        """
        remove BorgBackup installation
        """
        borg_dst_bin = BORG_DST_PATH / 'borg'
        if not borg_dst_bin.exists():
            print(f'Symlink "{borg_dst_bin}" does not exists, ok.')
        else:
            print(f'Remove "{borg_dst_bin}" symlink.')
            borg_dst_bin.unlink()

        if not BORG_ENV_PATH.exists():
            print(f'venv "{BORG_ENV_PATH}" does not exists, ok.')
        else:
            print(f'Remove venv "{BORG_ENV_PATH}"...')
            shutil.rmtree(BORG_ENV_PATH)

        verbose_check_call(
            info='Mark dependencies as "auto" installed.',
            command=f'apt-mark auto {APT_PACKAGES}',
        )
        verbose_check_call(
            info='Remove unused dependencies.',
            command='apt autoremove',
        )

    def _update_venv_pip(self):
        verbose_check_call(info='Update pip in venv', command=f'{VENV_PIP_PATH} install --upgrade pip wheel')

    def _update_symlinks(self):
        symlink(file_path=BORG_VENV_PATH, destination=BORG_DST_PATH)
        verbose_check_call(info='', command=f'borg --version')


if __name__ == '__main__':
    uid = os.getuid()
    if uid != 0:
        print(f'ERROR: UID: {uid!r} is not 0')
        print('ERROR: start this shell via sudo!')
        sys.exit(-1)

    BorgInstallShell().cmdloop()
