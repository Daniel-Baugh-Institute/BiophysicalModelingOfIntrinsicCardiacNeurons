#!/bin/bash
numproc=$1; if [ -z $numproc ]; then numproc=4; fi # Number of processes to use

echo $numproc
for (( i=1; i<=$numproc; i++ ))
    do
        echo "Running batch process $i ..."
        tmux new -d 'nice python3 batchNTE.py' \; pipe-pane 'cat > optLog${i}.txt'
        #screen -L -Logfile optLog$i.txt -d -m nice python3 batchNTE.py @# Run the models
        sleep 10
    done
