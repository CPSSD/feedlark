#!/bin/bash
# USAGE: bash install.sh

# Installs the required python modules by creating a virtualenv in /home/python
WORKING_DIR="/home/python"

# If virtualenv fails, install it with apt get and try again
virtualenv -p --system-site-packages python2 $WORKING_DIR || {
  apt-get -y update;
  apt-get -y install python-virtualenv;
  virtualenv -p --system-site-packages python2 $WORKING_DIR;
}

source $WORKING_DIR/bin/activate

pip2 install -r /vagrant/script/python/requirements.txt
python2 -m spacy.en.download

deactivate  # this is added to the path when activate is sourced

chown -R vagrant:vagrant $WORKING_DIR
