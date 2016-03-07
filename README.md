Feedlark
========

Simple and Sharp RSS Reader.


Dependencies
------------

- Vagrant
- VirtualBox

Vagrant Usage
-------------

For windows users, `vagrant ssh` doesn't work _straight_ away. Please read:
https://github.com/Varying-Vagrant-Vagrants/VVV/wiki/Connect-to-Your-Vagrant-Virtual-Machine-with-PuTTY

```sh
$ vagrant up # start
$ vagrant provision  # setup depends
$ vagrant ssh # gain ssh (on a POSIX system)
$ vagrant halt # stop
```

#### Running the whole application stack

Run the following commands inside your user folder or equivalent:

```sh
$ cd <root_of_your_repo>
$ vagrant up
$ script/start.sh
# if you get errors, ssh to the vagrant box and try:
$ cd /vagrant && bash script/start_internal.sh
```

### Vagrantfile

This will download an image of Ubuntu 15.10 (Wily), install the required
packages and setup the services.

Pip dependencies will also be downloaded.

#### IPs & Ports

- `192.168.2.2`: All services
- `3000`: ExpressJS Web Server
- `4730`: Gearman Job Server
- `27017`: MongoDB

#### Symbolic Links

The following symlinks your github repository into your Vagrant box's file system:

- `. -> /vagrant`

Is something missing from the Vagrant? Open an issue!

Project Directory Overview
--------------------------

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
