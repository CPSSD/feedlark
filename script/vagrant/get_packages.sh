#!/bin/sh

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y gcc-4.8 g++-4.8
sudo apt-get install -y python-software-properties
sudo apt-get install -y python3
sudo apt-get install -y python-pip
sudo apt-get install -y python-dev
sudo apt-get install -y python-sklearn
sudo apt-get install -y gearman-job-server
sudo service gearman-job-server start
sudo apt-get install -y git
sudo apt-get install -y golang
sudo apt-get install -y nodejs
sudo apt-get install -y build-essential
sudo apt-get upgrade -y
sudo apt-get autoremove
sudo apt-get clean
