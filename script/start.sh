#!/bin/bash
echo "Sending commands to Vagrant..."
vagrant ssh -c 'cd /vagrant && /vagrant/script/start_internal.sh'
