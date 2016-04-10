#!/bin/bash
echo "Sending commands to Vagrant..."
cd /vagrant
vagrant ssh -c /vagrant/script/start_internal.sh
