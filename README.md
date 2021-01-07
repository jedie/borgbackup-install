# BorgBackup-install

Simple Python script to install/update [borg backup](https://github.com/BorgBackup/borg)

What is does:

* install dependencies (for Debian / Ubuntu)
* Install/update Borg in venv into: `/opt/borgbackup-env/`
* Create symlink in `/usr/local/bin/borg`

So `borg` should be callable everywhere ;)

`borg-install.py` is a cli and a shell.


## get the sources

e.g.:

```bash
~$ git clone https://github.com/jedie/BorgBackup-install.git
~$ cd BorgBackup-install
~/BorgBackup-install$ $ sudo ./borg-install.py help
Welcome to BordBackup install shell


Documented commands (type help <topic>):
 help        - List available commands with 'help' or detailed help with 'help command'.
 install     - install BorgBackup using virtualenv and pip
 quit        - Exit this shell. (Or just hit Ctrl-C ;)
 uninstall   - remove BorgBackup installation
 update      - update BorgBackup installation
```


## install

To install dependencies for Debian / Ubuntu, create virtualenv and symlinks, call:

```bash
~/borgbackup-install$ sudo ./borg-install.py 
Welcome to BordBackup install shell


Documented commands (type help <topic>):
 help        - List available commands with 'help' or detailed help with 'help command'.
 install     - install BorgBackup using virtualenv and pip
 quit        - Exit this shell. (Or just hit Ctrl-C ;)
 uninstall   - remove BorgBackup installation
 update      - update BorgBackup installation

(borg-install) apt_install


____________________________________________________________________________________________________
 *** install the dependencies for Debian / Ubuntu ***
(call: 'apt-get install python3 python3-dev python3-pip python3-virtualenv libssl-dev openssl libacl1-dev libacl1 build-essential libfuse-dev fuse pkg-config')

...
____________________________________________________________________________________________________
 *** Create venv in "/opt/borgbackup-env" ***
(call: 'python3 -m venv /opt/borgbackup-env')
...

____________________________________________________________________________________________________
 *** Update pip in venv ***
(call: '/opt/borgbackup-env/bin/pip3 install --upgrade pip wheel')
...

____________________________________________________________________________________________________
 *** Install "borgbackup[fuse]" via pip ***
(call: '/opt/borgbackup-env/bin/pip3 install borgbackup[fuse]')

Collecting borgbackup[fuse]
  Using cached borgbackup-1.1.15-cp38-cp38-linux_x86_64.whl
Collecting llfuse>=1.3.4
  Using cached llfuse-1.3.8-cp38-cp38-linux_x86_64.whl
Installing collected packages: llfuse, borgbackup
Successfully installed borgbackup-1.1.15 llfuse-1.3.8


 *** Symlink "/opt/borgbackup-env/bin/borg" to "/usr/local/bin" ***

____________________________________________________________________________________________________
(call: 'borg --version')

borg 1.1.15
```


## update

```bash
~/borgbackup-install$ sudo ./borg-install.py update
...
```

## update

```bash
~/borgbackup-install$ sudo ./borg-install.py uninstall
...
```