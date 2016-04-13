Feedlark
========

Simple and Sharp RSS Reader.

Feedlark uses [Vagrant](http://vagrantup.com). Vagrant is a tool to deploy a virtual machine with our required environment fully configured. It requires Virtualbox to host the VM. The Vagrant startup script can be seen in `Vagrantfile`. You can start Vagrant with the instructions in the 'Usage' section below.

Once the environment is set up, Feedlark uses the [Gearman](http://gearman.org) application framework. Gearman allows different modules of the project to be run as separate applications called Workers. These Workers can then be requested to complete their task by a Client. The Gearman Job Server, initiated by Vagrant, handles the communication between each module. All of our Gearman data is transmitted in [BSON](https://en.wikipedia.org/wiki/BSON). The format of the data required by each worker is listed in its individual `README.md` file.

Feedlark is using [MongoDB](http://mongodb.org) for its data storage. There are Gearman workers in the `dbtools` directory to handle most database interactions, so that each individual module doesn't need to re-implement database connections.

The front end uses [express.js](http://expressjs.com/), an MVC framework in Node.js.

Setting up the Vagrant VM for the first time is very very slow (potentially upwards of 30 minutes), as there are a lot of dependencies. In particular, `spacy`, the tool we are using for Python natural language processing, requires a 500mb download of its English NLP model. However, once this initial setup has been completed, the VM can be booted in less than a minute.

The whole virtual machine will currently be no larger than 6Gb on disc. It will use at max 3GB of RAM.


Dependencies
------------

- Vagrant
- VirtualBox

Vagrant
-------------

```sh
$ vagrant up # start
$ vagrant provision  # setup depends
$ vagrant ssh # gain ssh (on a POSIX system)
$ vagrant halt # stop
```

#### Windows Issues

-  `vagrant ssh` doesn't always work unless you have an ssh binary.
  Please read
[this](https://github.com/Varying-Vagrant-Vagrants/VVV/wiki/Connect-to-Your-Vagrant-Virtual-Machine-with-PuTTY)
to setup putty.

- `CRLF` line endings may appear in your files. This will make the scripts error. 
  To fix this run these commands inside your host repository:
  ```
  git config core.eol lf
  git config core.autocrlf input
  git checkout-index --force --all
  ```
  Note that you'll need a text editor that supports `LF` to edit the files now on Windows.

#### Running the whole application stack

Run the following commands inside your user folder or equivalent:

```sh
$ cd <root_of_your_repo>
$ vagrant up
$ script/start.sh SECRET_KEY_HERE
# if you get errors, ssh to the vagrant box and try:
$ cd /vagrant && bash script/start_internal.sh
```

### Vagrant Configuration

The Vagrant configuration is laid out in the `Vagrantfile`.

This will download an image of Ubuntu 15.10 (Wily), install the required
packages and setup the services.

Pip dependencies will also be downloaded.

#### IPs & Ports

- `192.168.2.2`: All services
- `3000`: ExpressJS Web Server
- `4730`: Gearman Job Server
- `9001`: MongoDB

#### Symbolic Links

The following symlinks your github repository into your Vagrant box's file system:

- `. -> /vagrant`

Is something missing from the Vagrant? Open an issue!

Project Directory Overview
--------------------------

#### `./aggregator`

This is the code that coalesces the database collections `feed` and `user`, and places the data in `g2g`. That is, it takes the feed data, and the user data, and creates the feeds tailored to each individual user. It also includes the tool to compute the similarity of a user's interests and an article's topics.

#### `./dbtools`

The code that provides the Gearman database workers `db-add`, `db-get`, `db-update`, and `db-upsert`. The workers are written in Go.

#### `./doc`

This is where all documentation lives that doesn't directly relate to code. Find the specs for the database collections, and the logging specs, here.

#### `./scheduler`

A simple Gearman cron-like job that refreshes the feeds at regular intervals.

#### `./scraper`

This contains the Gearman worker to scrape feeds from the web.

#### `./script`

This is where we keep the scripts and configs related to the project. For example, the scripts to run the tests on all aspects of the project are here.

#### `./server`

This is where we keep the server, which routes HTTP and renders responses.

#### `./topics`

This contains the tool to parse an article and pick out the topics it relates to.

#### `./update_opinion`

This contains the tool that is called whenever a user votes on an article. It updates the list of topics they have opinions on in the database, and updates that user's machine learning model with the new data.
