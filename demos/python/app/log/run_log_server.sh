#!/usr/bin/env bash

set -u

cur_dir=`dirname $0`
cd $cur_dir

if [[ $# != 1 ]]; then
    echo "Usage: sh $0 action
        action: start, stop, restart, check_process
        ex. sh $0 restart"
    exit 1
fi

function check_process {
    ps aux | grep "$1" | grep -v "grep"
    if [[ $? = 0 ]]; then
        echo "$1 is running"
    else
        echo "\"$1\" stopped, please check!!!"
        echo "start app log:"
        cat $1.log
        return 0
    fi
}

function start {
    PYTHONPATH=../../ nohup python $1 >$1.log 2>&1 &

    sleep 2
    check_process $1
}

function stop {
    echo "Stopping" $1
    for pid in `ps aux | grep python | grep $1 | awk '{print $2}'`; do
        kill $pid
    done
}


function restart {
    stop $@
    start $@
}

# cmd
$1 "$(pwd)/multiprocess_file_logger.py"
