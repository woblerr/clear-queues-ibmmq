#!/bin/bash

image="ibmcom/mq:9.1.2.0"

set -x

docker pull ${image}
docker build -t mq_test -f tests/Dockerfile .

container_id=$(docker container run --env LICENSE=accept --env MQ_QMGR_NAME=QM1 --publish 1414:1414 --publish 9443:9443 --detach mq_test)

sleep 60

printf "Run unit tests"

docker container exec -it ${container_id} /bin/bash ./tests/prep_env.sh
docker container exec -it ${container_id} python2.7 -m pytest --cov=.

container_id=$(docker container run --env LICENSE=accept --env MQ_QMGR_NAME=QM1 --publish 1415:1414 --publish 9444:9443 --detach mq_test)

sleep 60

docker container exec -it ${container_id} /bin/bash ./tests/prep_env.sh
docker container exec -it ${container_id} python3.6 -m pytest --cov=.
