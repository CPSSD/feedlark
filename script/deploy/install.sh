ENVIRONMENT="PRODUCTION"

if [ $(id -u) -ne 0 ]; then
  echo "This file installs system files. Please run as root."
  exit 1
fi

grep -q -F 'ENVIRONMENT="PRODUCTION"' /etc/environment || echo  'ENVIRONMENT="PRODUCTION"' >> /etc/environment

# mongo has to be installed manually
sudo ./script/vagrant/get_packages.sh
sudo ./script/vagrant/server_install.sh
sudo ./script/vagrant/go_install.sh
sudo ./script/python/install.sh
