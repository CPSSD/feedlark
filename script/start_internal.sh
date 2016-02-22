#!/bin/bash
echo "Starting backend elements in screen sessions"
cd /vagrant
mkdir -p log/backend-getter
cd log/backend-getter
screen -dmLS backend-getter python /vagrant/dbtools/getter/getter.py
cd ..
mkdir -p backend-workers
cd backend-workers
screen -dmLS backend-workers go run /vagrant/dbtools/start_workers.go
cd ..
mkdir -p backend-aggregator
cd backend-aggregator
screen -dmLS backend-aggregator python /vagrant/aggregator/aggregator.py
cd ..
mkdir -p backend-scraper
cd backend-scraper
screen -dmLS backend-scraper python /vagrant/scraper/gman_scraper.py
cd ..
mkdir -p backend-scheduler
cd backend-scheduler
screen -dmLS backend-scheduler python /vagrant/scheduler/scheduler.py
echo "Starting frontend elements in screen sessions"
cd /vagrant/server
screen -dmLS frontend-sails /usr/bin/npm run start
echo "Running! Please allow ~20 seconds for everything to initialise"
echo "Running screens (Should be 6):"
sleep 1
screen -list