# Cleanup IBM MQ queues script

[![Actions Status](https://github.com/woblerr/clear-queues-ibmmq/workflows/GitHub%20CI/badge.svg)](https://github.com/woblerr/clear-queues-ibmmq/actions)

The script for deleting messages from queues (except SYSTEM) on local running mq managers.
Without arguments the script find all local running mq managers and clearing all non SYSTEM queues.
For clearing queues on specific managers or clearing specific queues - use script arguments.

## Install

```bash
pip install requirements.txt
```

## Usage

* Print help

```bash
python clear_queues_ibmmq.py -h

usage: python clear_queues_ibmmq.py [-m qmgrName] [-q queueName [queueName ...]] --qload

Delete messages from queues (except SYSTEM) on running local mq managers.
Without arguments the script find all local mq managers and clearing all non SYSTEM queues.
For clearing queues on specific managers or clearing specific queues - use script arguments.

optional arguments:
  -h, --help            show this help message and exit
  -m [qmgrName]         queue manager name
  -q [queueName [queueName ...]]
                        queue name
  --qload               usage qload utility
```

* Clear all queues for all managers

```bash
python clear_queues_ibmmq.py
```

* Clear all queues on specific manager

```bash
python clear_queues_ibmmq.py -m QM1
```

* Clear specific queues on all manager

```bash
python clear_queues_ibmmq.py -q DEV.QUEUE.1
```

* Clear queues when objects in use

    To use `qload` (`dmpmqmsg`) for clearing used queues you need to install [Supportpac MO03](https://www.ibm.com/support/pages/withdrawn-mo03-websphere-mq-queue-load-unload-utility) (integrated into MQ v8.0)  and  to add command path to env.\
    The script uses qload only if queue in use.

```bash
python clear_queues_ibmmq.py --qload
```

* Use simple regex

```bash
python clear_queues_ibmmq.py -m Q* -q DEV.QUEUE.* DEV.DEAD.LETTER.QUEUE
```

Sample output:

```bash
The DEV.QUEUE.1 queue on the QM1 manager has been cleared
The DEV.QUEUE.2 queue on the QM1 manager has been cleared
The DEV.QUEUE.3 queue on the QM1 manager has been cleared
The DEV.DEAD.LETTER.QUEUE queue on the QM1 manager has been cleared
```
