# borgbackup-poetry

fake project to install and use [borg backup](https://github.com/borgbackup/borg) via [poetry](https://python-poetry.org/) and a `Makefile`:

* [install the dependencies for Debian / Ubuntu via `apt-get`](https://borgbackup.readthedocs.io/en/stable/installation.html#debian-ubuntu)
* install `borg` in virtualenv via Poetry 
* link `borg` into `PATH` e.g.: `~/.local/bin/`

So `borg` is callable from everywhere and it's easy to update ;)

## install

Get the helper sources:

```bash
~$ git clone https://github.com/jedie/borgbackup-poetry.git
~$ cd borgbackup-poetry
~/borgbackup-poetry$ make
install-poetry         install or update poetry
apt-get-install        install the dependencies for Debian / Ubuntu
install                install project via poetry
update                 update the sources and installation
```


To install borg backup call this:

* `make install-poetry`
* `make apt-get-install`
* `make install`

e.g.:

```bash
~/borgbackup-poetry$ make install-poetry
pip3 install -U pip
...
pip3 install -U poetry
...

~/borgbackup-poetry$ make apt-get-install
sudo apt-get install python3 python3-dev python3-pip python3-virtualenv \
libssl-dev openssl \
libacl1-dev libacl1 \
build-essential \
libfuse-dev fuse pkg-config
...

~/borgbackup-poetry$ make install
...
Installing dependencies from lock file

Package operations: 2 installs, 0 updates, 0 removals

  • Installing llfuse (1.3.8)
  • Installing borgbackup (1.1.15)
  
poetry run python3 link_helper.py

Symlink "borg" and "borgfs" into PATH...

"borg" found in "~/.cache/pypoetry/virtualenvs/borgbackup-poetry-sCSN7rR2-py3.8/bin/borg".
"borgfs" found in "~/.cache/pypoetry/virtualenvs/borgbackup-poetry-sCSN7rR2-py3.8/bin/borgfs".
"poetry" found in "~/.local/bin/poetry".
 * Use bin path: "~/.local/bin"
 * Symlink "~/.cache/pypoetry/virtualenvs/borgbackup-poetry-sCSN7rR2-py3.8/bin/borg" to "~/.local/bin/borg"
 * Symlink "~/.cache/pypoetry/virtualenvs/borgbackup-poetry-sCSN7rR2-py3.8/bin/borgfs" to "~/.local/bin/borgfs"

You can now call "borg" and "borgfs" from commandline!

~/borgbackup-poetry$ cd
~$ borg --version
borg 1.1.15
```

## update

Just update the helper sources and borg e.g.:

```bash
~$ cd borgbackup-poetry
~/borgbackup-poetry$ make update
```