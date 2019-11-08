FROM ibmcom/mq:9.1.2.0 as mq_with_python
USER root
RUN set -ex && \
    apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update
RUN set -ex && \
    apt-get -y install \
    python2.7 \
    python3.6  
RUN set -ex && \
    apt-get install wget && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python2.7 get-pip.py && \
    python3.6 get-pip.py && \
    rm get-pip.py && \
    apt-get clean && \
    rm -r /var/lib/apt/lists/*
RUN mkdir -p /home/mqm && chown mqm:mqm /home/mqm
FROM mq_with_python
ARG SCRIPT_FOLDER=/home/mqm/admin/clear_queues_ibmmq
RUN mkdir -p $SCRIPT_FOLDER/tests
COPY ./requirements.txt $SCRIPT_FOLDER/requirements.txt
WORKDIR $SCRIPT_FOLDER
RUN pip2.7 --no-cache-dir install -r $SCRIPT_FOLDER/requirements.txt && \
    pip3.6 --no-cache-dir install -r $SCRIPT_FOLDER/requirements.txt
COPY ./clear_queues_ibmmq.py $SCRIPT_FOLDER
COPY ./tests/test_clear_queues_ibmmq.py $SCRIPT_FOLDER/tests
COPY ./tests/prep_env.sh $SCRIPT_FOLDER/tests/prep_env.sh
RUN chmod 744 $SCRIPT_FOLDER/tests/prep_env.sh
RUN chown -R mqm:mqm $SCRIPT_FOLDER
USER mqm
ENTRYPOINT ["runmqdevserver"]