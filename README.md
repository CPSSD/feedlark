# Feedlark 

Simple and Sharp RSS Reader

Development Environment
============

Dependencies
------------

- Vagrant
- VirtualBox

Included Packages
------------

	Git
	MongoDB v3.2+
	Gearman Job Server
	Go Compiler (& GOPATH)
	Python 2.7+ & 3.4+
	Pip for Python 2 + 3
	Python package "feeparser"
	Python package "beautifulsoup4"
	Python package "requests"
	Python package "gearman"
	Python package "virtualenv"
	Python package "pymongo"
	NodeJS 4.3
	NPM
	NodeJS packages from "server" directory
	OpenJDK 7
	Scala 2.11

Something missing? Open an issue with the following content:

- Title: Add ~package~ to development environment
- Purpose of package
- Install command, if readily available

Setup
------------

Run the following commands inside your user folder or equivalent

	$ cp Vagrantfile /home/Vagrant/Vagrantfile
	$ cd /home/Vagrant/Vagrantfile
	$ vagrant up

This will download an image of Ubuntu 15.10 (Wily), install the required packages and setup the services. Pip dependencies will also be downloaded
It will also make the following local symlinks

- `. -> /vagrant`

Usage
------------

To start the box:

	$ vagrant up

To update an existing box (after starting):

	$ vagrant provision

To gain SSH access:

	$ vagrant ssh

To stop the box:

	$ vagrant halt

MongoDB is forwarded/exposed on port `27017`

The Gearman job server runs on port `4730`

All services are also exposed on the IP `192.168.2.2`

Startup
------------

To start the program, run the following commands (NOT IN VAGRANT):

	$ cd <root_of_your_repo>
	$ script/start.sh

