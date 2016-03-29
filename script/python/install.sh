#!/bin/bash
# USAGE: bash install.sh <install_directory>

# Installs the required python modules by creating a virtualenv in
# WORKING_DIR, which is by default /home/python
# Also installs an env file in this folder that points at the used env directory

export WORKING_DIR=${1:-"/home/python"}

# If virtualenv fails, install it with apt get and try again
virtualenv -p python2 $WORKING_DIR || { apt-get -y update; apt-get -y install python-virtualenv; virtualenv -p python2 $WORKING_DIR; }

source $WORKING_DIR/bin/activate

pip2 install -r /vagrant/script/python/requirements.txt
python2 -m spacy.en.download

# this ensures we know where the env is regardless of install location
ln -s $WORKING_DIR /vagrant/script/python/env

deactivate  # this is added to the path when activate is sourced

chown -R vagrant:vagrant $WORKING_DIR
chown vagrant:vagrant /vagrant/script/python/env
