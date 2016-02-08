Feedlark:tm: Development Environment
============

Dependencies
------------

- Vagrant
- VirtualBox

Included Packages
------------

	Nginx
	MongoDB
	Gearman Job Server
	Go Compiler
	Python 2, 3 + 3.5
	Pip 3
	Python 3 package "feeparser"
	Python 3 package "beautifulsoup4"
	Python 3 package "requests"

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

- `html -> /var/www/html`
- `python -> /home/python`

Usage
------------

To start the box:

	$ vagrant up

To gain SSH access:

	$ vagrant ssh

To stop the box:

	$ vagrant halt

All other services (Nginx, mongoDB) should be exposed on the IP `192.168.2.2`

Use the `html` folder to store any web hosted files

Use the `python` folder to sync scripts