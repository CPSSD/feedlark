#! /bin/sh

mkdir -p /home/vagrant/.mongodb
chmod 755 /home/vagrant/.mongodb
chown -R vagrant:vagrant /home/vagrant
chown -R mongodb:mongodb /home/vagrant/.mongodb
sudo mv /etc/mongod.conf /etc/mongod.conf.orig
sudo rm -f /etc/mongod.conf
sudo cp /vagrant/script/vagrant/mongod.conf /etc/mongod.conf
sudo systemctl enable mongod
sudo systemctl start mongod
sudo systemctl enable gearman-job-server
sudo systemctl start gearman-job-server
mongo /vagrant/script/vagrant/create_feed_user_db.js
