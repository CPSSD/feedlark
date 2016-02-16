# The 2 is the config version file
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/wily64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = true

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 27017, host: 27017

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.2.2"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
     vb.memory = "1024"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # ^^^ We should look at this for our eventual deploy --devoxel

  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Add mongodb config
  config.vm.provision "file", source: "script/vagrant/mongod.conf", destination: "/tmp/mongod.conf"

  # Make sure the swap is up before installs
  config.vm.provision "shell", path: "script/vagrant/create_swap.sh"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.

  # Should we move and seperate all this stuff to script/vagrant? -- devoxel
  config.vm.provision "shell", inline: <<-SHELL
    sudo echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y gcc-4.8 g++-4.8
    sudo apt-get install -y python-software-properties
    sudo apt-get install -y mongodb-org
    sudo apt-get install -y python3
    sudo apt-get install -y python-pip
    sudo apt-get install -y python-dev
    sudo apt-get install -y gearman-job-server
    sudo apt-get install -y git
    sudo apt-get install -y golang
    sudo apt-get install -y nodejs
    sudo apt-get install -y build-essential
    sudo apt-get install -y openjdk-7-jdk
    sudo apt-get install -y scala
    sudo apt-get upgrade -y
    sudo apt-get autoremove
    sudo apt-get clean
    sudo pip install feedparser
    sudo pip install beautifulsoup4
    sudo pip install requests
    sudo pip install virtualenv
    sudo pip install gearman
    sudo pip install pymongo
    npm cache clean
    cd /vagrant/server && npm install -y --no-bin-links
    echo "export GOPATH=/home/vagrant/.go" > /home/vagrant/.profile
    mkdir -p /home/vagrant/.go
    mkdir -p /home/vagrant/.mongodb
    chmod 755 /home/vagrant/.mongodb
    chown -R vagrant:vagrant /home/vagrant
    chown -R mongodb:mongodb /home/vagrant/.mongodb
    sudo mv /etc/mongod.conf /etc/mongod.conf.orig
    sudo rm -f /etc/mongod.conf
    sudo mv /tmp/mongod.conf /etc/mongod.conf
    sudo systemctl enable mongod
    sudo systemctl start mongod
    sudo systemctl enable gearman-job-server
    sudo systemctl start gearman-job-server
  SHELL

end
