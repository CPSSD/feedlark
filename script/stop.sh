#!/bin/bash
echo "Sending commands to Vagrant..."
vagrant ssh -c /vagrant/script/stop_internal.sh
