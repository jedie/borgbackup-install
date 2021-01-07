"""
    Just link "borg" and "borgfs" into PATH.
    So the user can call it everywhere ;)
"""
import os
import shutil
from pathlib import Path


def get_bin_path(file_name):
    raw_path = shutil.which(file_name)
    assert raw_path, f'"{file_name}" not found in PATH!'
    path = Path(raw_path)
    print(f'"{file_name}" found in "{short_home_path(path)}".')
    return path


def symlink(file_path, destination):
    destination = Path(destination, file_path.name)
    print(f' * Symlink "{short_home_path(file_path)}" to "{short_home_path(destination)}"')

    if destination.is_file():
        # remove existing symlink to "refresh" it
        destination.unlink()

    destination.symlink_to(file_path)


def short_home_path(path):
    home = Path.home()
    relative_path = path.relative_to(home)
    if relative_path != path:
        return f'~/{relative_path}'
    return path


def main():
    assert 'VIRTUAL_ENV' in os.environ, 'VIRTUAL_ENV not in environment! Call be only via poetry run!'

    borg_path = get_bin_path(file_name='borg')
    borgfs_path = get_bin_path(file_name='borgfs')

    poetry_path = get_bin_path(file_name='poetry')
    bin_path = poetry_path.parent
    print(f' * Use bin path: "{short_home_path(bin_path)}"')

    symlink(file_path=borg_path, destination=bin_path)
    symlink(file_path=borgfs_path, destination=bin_path)


if __name__ == '__main__':
    print('\nSymlink "borg" and "borgfs" into PATH...\n')
    main()
    print('\nYou can now call "borg" and "borgfs" from commandline!')
