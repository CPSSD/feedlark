#!/bin/bash
echo "Starting backend elements in screen sessions"
cd /vagrant

# this includes the python env binaries over system wide ones
source /vagrant/script/python/env/bin/activate

# first one should be in log/XYZ, the rest of them then cd to this new log/ dir
# and create their own subdirs from there
mkdir -p log/backend-db-workers
cd log/backend-db-workers
screen -dmLS backend-db-workers go run /vagrant/dbtools/start_workers.go
cd ..
mkdir -p backend-aggregator
cd backend-aggregator
screen -dmLS backend-aggregator python /vagrant/aggregator/aggregator.py
cd ..
mkdir -p backend-scraper
cd backend-scraper
screen -dmLS backend-scraper python /vagrant/scraper/scraper.py
cd ..
mkdir -p backend-update-opinion
cd backend-update-opinion
screen -dmLS backend-update-opinion python /vagrant/update_opinion/updater.py
cd ..
mkdir -p backend-topics
cd backend-topics
screen -dmLS backend-topics python /vagrant/topics/topics.py
cd ..
mkdir -p backend-scheduler
cd backend-scheduler
screen -dmLS backend-scheduler python /vagrant/scheduler/scheduler.py
cd ..
mkdir -p backend-art-getter
cd backend-art-getter
screen -dmLS backend-art-getter python /vagrant/article_getter/gman_art_getter.py
echo "Starting frontend elements in screen sessions"
cd /vagrant/server
screen -dmLS frontend-express /usr/bin/npm run start
echo "Running! Please allow ~20 seconds for everything to initialise"
echo "Running screens:"
sleep 1
screen -list
