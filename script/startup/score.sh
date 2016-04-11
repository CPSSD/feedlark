#!/bin/bash
# should be run by start_internal, otherwise this relative path is wrong.
source /home/python/bin/activate
python ../../aggregator/kw_score.py
