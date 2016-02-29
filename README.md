Feedlark
========

Simple and Sharp RSS Reader.

Feedlark uses [Vagrant](http://vagrantup.com). Vagrant is a tool to deploy a virtual machine with our required environment fully configured. It requires Virtualbox to host the VM. The Vagrant startup instructions can be seen in the `Vagrantfile` script.

Once the environment is set up, Feedlark uses the [Gearman](http://gearman.org) application framework. Gearman allows different modules of the project to be run as separate applications called Workers. These Workers can then be requested to complete their task by a Client. The Gearman Job Serveri, initiated by Vagrant, handles the communication between each module. All of our Gearman data is transmitted in [BSON](https://en.wikipedia.org/wiki/BSON). The format of the data required by each worker is listed in its individual `README.md` file.

Feedlark is using [MongoDB](http://mongodb.org) for its data storage. There are Gearman workers in the `dbtools` directory to handle most database interactions, so that each individual module doesn't need to re-implement database connections.

The front end uses [Sails.js](http://sailsjs.org), an MVC framework in Node.js.

Dependencies
------------

- Vagrant
- VirtualBox

Usage
------------

For windows users, `vagrant ssh` doesn't work _straight_ away. Please read:
https://github.com/Varying-Vagrant-Vagrants/VVV/wiki/Connect-to-Your-Vagrant-Virtual-Machine-with-PuTTY

```sh
$ vagrant up # start
$ vagrant provision  # setup depends
$ vagrant ssh # gain ssh (on a POSIX system)
$ vagrant halt # stop
```

### Vagrantfile

This will download an image of Ubuntu 15.10 (Wily), install the required
packages and setup the services.

Pip dependencies will also be downloaded.

#### Ports

- `27017`: MongoDB is forwarded/exposed on port
-  `4730`: The Gearman job server runs on port
- `192.168.2.2`: All services are also exposed on the IP

#### Symlinks


- `. -> /vagrant`

Is something missing from the Vagrant? Open an issue!

#### Running the whole application stack

Run the following commands inside your user folder or equivalent:

```sh
$ cd <root_of_your_repo>
$ vagrant up
$ script/start.sh
# if you get errors, ssh to the vagrant box and try:
$ cd /vagrant && bash script/start_internal.sh
```

Project Directory Overview
---------------------------

#### `./aggregator`

This is the code that ties the three Feedlark databases together, it coalesces
`feed` and `user` and places the data in `g2g`.

#### `./dbtools`

This is we implement gearman mongo-db workers.

#### `./doc`

This is where all documentation lives that doesn't directly relate to code.
Find all the specs here.

#### `./scheduler`

A simple gearman cron-like job that makes sure the workers are working.

#### `./scraper`

This is where we scrape from the web. This tool plays an important part in
getting information from individual feeds.

#### `./script`

This is where we keep scripts/confs, related to the project.

#### `./server`

This is where we keep the server, which routes HTTP and renders responses.
