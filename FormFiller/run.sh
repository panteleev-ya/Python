#!/bin/bash

kill -15 $(cat purchase-tracker.pid)
nohup python3 main.py &
echo $! > purchase-tracker.pid
