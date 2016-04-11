#!/bin/bash
if [ $# != '1' ]
    then
        echo "Please pass in a secret key as an argument"
        exit
fi
export SECRETKEY=$1

echo "Starting backend elements in screen sessions"
echo "Please run from root of project"

# first one should be in log/XYZ, the rest of them then cd to this new log/ dir
# and create their own subdirs from there

mkdir -p log/backend-db-workers
cd log/backend-db-workers
# currently in log/blabla so ../../ refers to root of project
screen -dmLS backend-db-workers /bin/bash ../../script/startup/dbtools.sh
cd ..

mkdir -p backend-aggregator
cd backend-aggregator
screen -dmLS backend-aggregator /bin/bash ../../script/startup/aggregator.sh
cd ..

mkdir -p backend-scraper
cd backend-scraper
screen -dmLS backend-scraper /bin/bash ../../script/startup/scraper.sh
cd ..

mkdir -p backend-update-opinion
cd backend-update-opinion
screen -dmLS backend-update-opinion /bin/bash ../../script/startup/updater.sh
cd ..

mkdir -p backend-topics
cd backend-topics
screen -dmLS backend-topics /bin/bash ../../script/startup/topics.sh
cd ..

mkdir -p backend-scheduler
cd backend-scheduler
screen -dmLS backend-scheduler /bin/bash ../../script/startup/scheduler.sh
cd ..

mkdir -p backend-art-getter
cd backend-art-getter
screen -dmLS backend-art-getter /bin/bash ../../script/startup/article_getter.sh
cd ..

echo "Starting frontend elements in screen sessions"
cd ../server
screen -dmLS frontend-express /bin/bash ../script/startup/frontend.sh

echo "Running! Please allow ~20 seconds for everything to initialise"
echo "Running screens:"
sleep 1
screen -list
