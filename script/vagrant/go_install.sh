#! /bin/sh

if [ "$ENVIRONMENT" = "PRODUCTION" ]; then
  echo "export GOPATH=/home/feedling/.go" > /home/vagrant/.profile
  mkdir -p /home/feedling/.go
  export GOPATH=/home/feedling/.go
else
  echo "export GOPATH=/home/vagrant/.go" > /home/vagrant/.profile
  echo "export PATH=/vagrant/server/node_modules/.bin:$PATH:" >> /home/vagrant/.profile
  mkdir -p /home/vagrant/.go
  export GOPATH=/home/vagrant/.go
fi

go get github.com/mikespook/gearman-go/worker
go get gopkg.in/mgo.v2
go get gopkg.in/mgo.v2/bson
