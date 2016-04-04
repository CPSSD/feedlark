#! /bin/sh

cd /vagrant/server
npm install -y
npm dedupe
npm cache clean

