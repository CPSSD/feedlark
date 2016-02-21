#!/bin/bash
echo "Starting backend elements in screen sessions"
cd /vagrant
screen -dmS backend-getter python dbtools/getter/getter.py
screen -dmS backend-workers go run dbtools/start_workers.go
screen -dmS backend-aggregator python aggregator/aggregator.py
screen -dmS backend-scraper python scraper/gman_scraper.py
screen -dmS backend-scheduler python scheduler/scheduler.py
echo "Starting frontend elements in screen sessions"
cd /vagrant/server
screen -dmS frontend-sails /usr/bin/npm run start
echo "Running! Please allow ~20 seconds for everything to initialise"
echo "Running screens (Should be 6):"
sleep 1
screen -list

