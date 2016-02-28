#!/bin/bash
echo "Stopping backend elements in screen sessions"
screen -S backend-db-workers -p 0 -X stuff ^C
screen -S backend-aggregator -p 0 -X stuff ^C
screen -S backend-scraper -p 0 -X stuff ^C
screen -S backend-scheduler -p 0 -X stuff ^C
echo "Stopping frontend elements in screen sessions"
screen -S frontend-sails -p 0 -X stuff ^C
echo "Stopped! Allowing 3 seconds grace period..."
sleep 3
echo "Running screens (Should be 0):"
screen -list
