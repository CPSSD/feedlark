#!/bin/bash
# Pulls the site onto the production server
cd /home/feedling/repo

mkdir -p log/updater
curdate=$(date +'%H:%M_%d\%m\%Y')
logfile=log/updater/$curdate.log
gitlog=log/updater/$curdate\_git.log

function print {
	curdate=$(date +'%H:%M %d\%m\%Y')
	echo "$curdate $1"
	echo "$curdate $1" >> $logfile
}

print "INFO: Starting update"

git pull > $gitlog

# Make sure that went well
if [ $? -ne 0 ]; then
	print "ERROR: Git pull failed!"
	exit 1
fi

print "INFO: Git pull successful"

# Check if the branch updated
grep up-to-date $gitlog
if [ $? -eq 0 ]; then
	print "INFO: Master up to date. Stopping"
	exit 0
fi

print "INFO: Stopping processes"
script/stop_internal.sh

# Check if NPM needs reinstalling
grep package.json $gitlog
if [ $? -eq 0 ]; then
	print "INFO: Updating NPM dependences"
	cd server
	npm install >> $logfile
	cd ..
fi

# Check if Python needs reinstalling
grep requirements.txt $gitlog
if [ $? -eq 0 ]; then
	print "INFO: Updating Python dependences"
	source /home/python/bin/activate
	pip2 install --ignore-installed -r script/python/requirements.txt >> $logfile
	deactivate
fi

print "INFO: Starting processes"
script/start_internal.sh

print "INFO: Finished update!"
