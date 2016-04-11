#!/bin/bash
# Pulls the site onto the production server
#cd /home/feedling/repo

mkdir -p log/updater
curdate=$(date +'%H:%M_%d\%m\%Y')
logfile=log/updater/$curdate.log
gitlog=log/updater/$curdate\_git.log

echo "INFO: Starting update" > $logfile

git pull > $gitlog

# Check if the branch updated
grep up-to-date $gitlog
if [ $? -eq 0 ]; then
	echo "INFO: Master up to date. Stopping" >> $logfile
	exit 0
fi

echo "INFO: Stopping processes" >> $logfile
script/stop_internal.sh

# Make sure that went well
if [ $? -ne 0 ]; then
	echo "ERROR: Git pull failed!" >> $logfile
	exit 1
fi

echo "INFO: Git pull successful" >> $logfile

# Check if NPM needs reinstalling
grep package.json $gitlog
if [ $? -eq 0 ]; then
	echo "INFO: Updating NPM dependences" >> $logfile
	cd server
	npm install >> $logfile
	cd ..
fi

# Check if Python needs reinstalling
grep requirements.txt $gitlog
if [ $? -eq 0 ]; then
	echo "INFO: Updating Python dependences" >> $logfile
	source /home/python/bin/activate
	pip2 install --ignore-installed -r script/python/requirements.txt >> $logfile
	deactivate
fi

echo "INFO: Starting processes" >> $logfile
script/start_internal.sh

echo "INFO: Finished update! Time: $(date +'%H:%M %D/%M/%Y')" >> $logfile

