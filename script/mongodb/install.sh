#!/bin/bash

# USAGE bash install.sh
# Installs mongodb 3.2 and configures it

echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
apt-get -y update
apt-get install -y mongodb-org

# /var/lib was chosen as dictated by the Filesystem Hierarchy Standard
mkdir -p /var/lib/mongodb
chmod 0755 /var/lib/mongodb
chown -R mongodb:mongodb /var/lib/mongodb
sudo mv /etc/mongod.conf /etc/mongod.conf.orig
sudo cp /vagrant/script/mongodb/mongod.conf /etc/mongod.conf

sudo service mongod start

if [ ! "$ENVIRONMENT" = "PRODUCTION" ]
  then
    mongo /vagrant/script/vagrant/populate_sample_data.js
fi
