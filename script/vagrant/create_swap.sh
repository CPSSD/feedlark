#!/bin/sh

# Credit to this file goes to Jorge Quilcate
#   http://jeqo.github.io/blog/devops/vagrant-quickstart/
#   Code is licensed under Apache License 2.0
#   See https://github.com/jeqo/jeqo.github.io/blob/master/LICENSE

# size of swapfile in megabytes
swapsize=1024

# does the swap file already exist?
grep -q "swapfile" /etc/fstab

# if not then create it
if [ $? -ne 0 ]; then
	echo 'swapfile not found. Adding swapfile.'
	fallocate -l ${swapsize}M /swapfile
	chmod 600 /swapfile
	mkswap /swapfile
	swapon /swapfile
	echo '/swapfile none swap defaults 0 0' >> /etc/fstab
else
	echo 'swapfile found. No changes made.'
fi

# output results to terminal
cat /proc/swaps
cat /proc/meminfo | grep Swap
