#! /bin/sh

echo "export GOPATH=/home/vagrant/.go" > /home/vagrant/.profile
echo "export PATH=/vagrant/server/node_modules/.bin:$PATH:" >> /home/vagrant/.profile
mkdir -p /home/vagrant/.go
export GOPATH=/home/vagrant/.go
go get github.com/mikespook/gearman-go/worker
go get gopkg.in/mgo.v2
go get gopkg.in/mgo.v2/bson

