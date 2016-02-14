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
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Add mongodb config
  config.vm.provision "file", source: "script/mongod.conf", destination: "/tmp/mongod.conf"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo curl -sL https://deb.nodesource.com/setup_4.x
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    sudo echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org python3 python3-pip gearman-job-server git golang nodejs npm build-essential
    sudo apt-get autoremove
    sudo apt-get clean
    sudo pip3 install feedparser
    sudo pip3 install beautifulsoup4
    sudo pip3 install requests
    sudo pip3 install virtualenv
    sudo pip3 install gearman
    sudo pip3 install pymongo
    sudo npm install -g mocha
    sudo npm install -g sails
    mkdir /home/vagrant/.go
    mkdir /home/vagrant/.mongodb
    chmod 777 /home/vagrant/.mongodb
    echo "export GOPATH=/home/vagrant/.go" >> /home/vagrant/.profile
    chown -R vagrant:vagrant /home/vagrant
    sudo mv /etc/mongod.conf /etc/mongod.conf.orig
    sudo mv /tmp/mongod.conf /etc/mongod.conf
    sudo systemctl enable mongod
    sudo systemctl start mongod
    sudo systemctl enable gearman-job-server
    sudo systemctl start gearman-job-server
  SHELL

end
