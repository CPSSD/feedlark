#!/bin/bash
echo "Sending commands to Vagrant..."
vagrant ssh -c /vagrant/script/start_internal.sh
