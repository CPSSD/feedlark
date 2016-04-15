#!/bin/bash
if [ $# != '1' ]
    then
        echo "Please pass in a secret key as an argument"
        exit
fi
echo "Sending commands to Vagrant..."
vagrant ssh -c 'cd /vagrant && export SECRETKEY=$1 && script/start_internal.sh'
