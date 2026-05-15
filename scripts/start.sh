#!/bin/bash
python3 $ALICE_PATH/scripts/set-theme.py
python3 $ALICE_PATH/scripts/moniter-daemon.py &
bash /home/neros/Documents/projects/screen-time/run &
