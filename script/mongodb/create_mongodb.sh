#!/bin/bash

# /var/lib was chosen as dictated by the Filesystem Hierarchy Standard
mkdir -p /var/lib/mongodb
chmod 0755 /var/lib/mongodb
chown -R mongodb:mongodb /home/vagrant/.mongodb
sudo mv /etc/mongod.conf /etc/mongod.conf.orig
sudo cp /vagrant/script/mongodb/mongod.conf /etc/mongod.conf
sudo systemctl enable mongod
sudo systemctl start mongod

if [ ! "$ENVIRONMENT" = "PRODUCTION" ]
  then
    mongo /vagrant/script/vagrant/populate_sample_data.js
fi
