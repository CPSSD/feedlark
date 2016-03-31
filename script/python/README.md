# Feedlark Python Environment

### Installation

Installation should be managed by Vagrant. Alternativly `install.sh` can be run
on any OS with `apt-get`, although only Ubuntu has been tested.

### Packages

See `requirements.txt`

### Environment

To keep the python install non-global, we use [virtualenv].

Packages are by default installed to `/home/python` on the vagrant machine.

This may change between environments however, so please use
`/vagrant/script/python/env` which, after installation, is a symbolic link to
the virtual environment.

[virtualenv]:https://virtualenv.pypa.io/en/latest/
