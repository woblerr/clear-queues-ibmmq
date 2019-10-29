FROM ibmcom/mq:9.1.2.0 as mq_with_python
USER root
RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && \
    apt-get autoclean
RUN apt-get -y install \
    python2.7 python2.7-dev \
    python3.6 python3.6-dev && \
    apt-get autoclean
RUN apt-get install wget && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python2.7 get-pip.py && \
    python3.6 get-pip.py && \
    rm get-pip.py && \
    apt-get autoclean
RUN mkdir -p /home/mqm && chown mqm:mqm /home/mqm
FROM mq_with_python
ARG SCRIPT_FOLDER=/home/mqm/admin/clear_queues_ibmmq
RUN mkdir -p $SCRIPT_FOLDER/tests
COPY ./requirements.txt $SCRIPT_FOLDER/requirements.txt
WORKDIR $SCRIPT_FOLDER
RUN pip2.7 install -r $SCRIPT_FOLDER/requirements.txt && \
    pip3.6 install -r $SCRIPT_FOLDER/requirements.txt
COPY ./clear_queues_ibmmq.py $SCRIPT_FOLDER
COPY ./tests/test_clear_queues_ibmmq.py $SCRIPT_FOLDER/tests
COPY ./tests/prep_env.sh $SCRIPT_FOLDER/tests/prep_env.sh
RUN chmod 744 $SCRIPT_FOLDER/tests/prep_env.sh
RUN chown -R mqm:mqm $SCRIPT_FOLDER
USER mqm
ENTRYPOINT ["runmqdevserver"]