#! /bin/sh

sudo su -c "gem install sass"
cd /vagrant/server
npm install -y
npm dedupe
npm cache clean

