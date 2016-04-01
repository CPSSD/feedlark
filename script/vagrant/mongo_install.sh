#! /bin/sh

mkdir -p /home/vagrant/.mongodb
chmod 755 /home/vagrant/.mongodb
chown -R vagrant:vagrant /home/vagrant
chown -R mongodb:mongodb /home/vagrant/.mongodb
sudo mv /etc/mongod.conf /etc/mongod.conf.orig
sudo rm -f /etc/mongod.conf
sudo cp /vagrant/script/vagrant/mongod.conf /etc/mongod.conf
sudo service mongod start
mongo /vagrant/script/vagrant/create_feed_user_db.js
