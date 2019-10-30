#!/bin/bash

set -x

bin_dir="/opt/mqm/samp/bin"

for i in {1..3}
    do
        echo "Test message $i" | $bin_dir/amqsput "DEV.QUEUE.$i" "QM1"
done

echo "Test message 4" | $bin_dir/amqsput "DEV.DEAD.LETTER.QUEUE" "QM1"
