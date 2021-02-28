FROM ibmcom/mq:9.2.0.0-r2 as mq_with_python
USER root
RUN set -ex && \
    microdnf install yum && \
    yum install -y python27 python36 && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN ln -sf /opt/mqm/bin/dmpmqmsg /usr/bin/dmpmqmsg
FROM mq_with_python
ARG SCRIPT_FOLDER=/opt/mqm/admin/clear_queues_ibmmq
# https://github.com/ibm-messaging/mq-container/blob/9.2.0/Dockerfile-server#L162
ARG WORK_USER=1001
RUN mkdir -p $SCRIPT_FOLDER/tests
COPY ./requirements.txt $SCRIPT_FOLDER/requirements.txt
WORKDIR $SCRIPT_FOLDER
RUN pip2.7 --no-cache-dir install -r $SCRIPT_FOLDER/requirements.txt && \
    pip3.6 --no-cache-dir install -r $SCRIPT_FOLDER/requirements.txt
COPY ./tests/prep_env.sh $SCRIPT_FOLDER/tests/prep_env.sh
RUN chmod 744 $SCRIPT_FOLDER/tests/prep_env.sh
COPY ./clear_queues_ibmmq.py $SCRIPT_FOLDER
COPY ./tests/test_clear_queues_ibmmq.py $SCRIPT_FOLDER/tests
RUN chown -R $WORK_USER:root $SCRIPT_FOLDER
USER $WORK_USER
ENTRYPOINT ["runmqdevserver"]