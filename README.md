Feedlark
========

Simple and Sharp RSS Reader.


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
