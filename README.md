# feedlark.com

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
	MongoDB
	Gearman Job Server
	Go Compiler (& GOPATH)
	Python 2 + 3
	Pip 3
	Python 3 package "feeparser"
	Python 3 package "beautifulsoup4"
	Python 3 package "requests"
	Python 3 package "gearman"
	Python 3 package "virtualenv"
	Python 3 package "pymongo"
	NodeJS
	NPM
	NodeJS packages from "server" directory

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

All other services (Nginx, MongoDB) should be exposed on the IP `192.168.2.2`

Use `python3` and `pip3` commands instead of their normal versions (which are 2.X based)

