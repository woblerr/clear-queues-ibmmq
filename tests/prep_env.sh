#!/bin/bash

set -x

for i in {1..3}
    do
        echo "Test message ${i}" | /opt/mqm/samp/bin/amqsput "DEV.QUEUE.${i}" "QM1"
done

echo "Test message 4" | /opt/mqm/samp/bin/amqsput "DEV.DEAD.LETTER.QUEUE" "QM1"
