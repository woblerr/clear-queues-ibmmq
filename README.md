# Clear IBM MQ queues script
[![Build Status](https://travis-ci.com/woblerr/clear-queues-ibmmq.svg?branch=master)](https://travis-ci.com/woblerr/clear-queues-ibmmq)

The script for deleting messages from queues (except SYSTEM) on local running mq managers.
Without arguments the script find all local running mq managers and clearing all non SYSTEM queues.
For clearing queues on specific managers or clearing specific queues - use script arguments.

## Install
```bash
pip install requirements.txt
```

## Usage
* Clear all queues for all managers
```bash
python clear_queues_ibmmq.py
```
* Clear all queues on specific manager
```bash
python clear_queues_ibmmq.py -m QM1
```
* Clear specific queues on specific manager
```bash
python clear_queues_ibmmq.py -q DEV.QUEUE.1
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