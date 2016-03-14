#!/bin/bash

export WORKING_DIR=/home/python

virtualenv $WORKING_DIR
chmod +x $WORKING_DIR/bin/*
$WORKING_DIR/bin/activate
$WORKING_DIR/bin/pip install -r /vagrant/script/requirements.txt
$WORKING_DIR/bin/python -m spacy.en.download
