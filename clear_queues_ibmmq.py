import argparse
import re
import sys
import subprocess


def run(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output = proc.communicate()[0]
    return output


def dis_qm(qm_name):
    if qm_name == 'all':
        command = 'dspmq'
    else:
        command = 'dspmq -m {}'.format(qm_name)
    return run(command)


def dis_qlocal(qs, qm):
    command = "echo 'DISPLAY QLOCAL({}) WHERE (CURDEPTH GE 1)'| runmqsc {}".format(qs, qm)
    return run(command)


def clear_qlocal(q, qm):
    command = "echo 'clear qlocal({})' | runmqsc {}".format(q, qm)
    return run(command)


def get_running_mq_manager(qm_name):
    running_qm = []
    name_regexp = r'QMNAME\(([^)]+)\)'
    status_regexp = r'STATUS\(Running\)'
    qms = dis_qm(qm_name)
    for item in filter(None, qms.split('\n')):
        if re.search(status_regexp, item):
            manager_name = re.search(name_regexp, item).group(1)
            running_qm.append(manager_name)
    return running_qm


def get_not_empty_queues(qs_list, qm):
    not_empty_qs = []
    if qs_list == 'all':
        qs_data = dis_qlocal('*', qm)
        not_empty_qs.append(list_non_system_qs(qs_data))
        return not_empty_qs
    for item in qs_list:
        qs_data = dis_qlocal(item, qm)
        not_empty_qs.append(list_non_system_qs(qs_data))
    return not_empty_qs


def list_non_system_qs(q_data):
    qs_for_clearing = []
    q_regexp = r'QUEUE\(([^)]+)\)'
    q_system_regexp = r'SYSTEM.'
    for item in q_data.split('Display Queue details'):
        if not item:
            continue
        q = re.search(q_regexp, item)
        if (q is not None and not re.search(q_system_regexp, q.group(1))):
            qs_for_clearing.append(q.group(1))
    return qs_for_clearing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python clear_queues_ibmmq.py',
        usage='python clear_queues_ibmmq.py [-m qmgrName] [-q queueName [queueName ...]]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
Delete messages from queues (except SYSTEM) on running local mq managers.
Without arguments the script find all local mq managers and clearing all non SYSTEM queues. 
For clearing queues on specific managers or clearing specific queues - use script arguments.
''')
    parser.add_argument('-m', metavar='qmgrName', nargs='?', default='all', dest='mq_manager_name', help='queue manager name')
    parser.add_argument('-q', metavar='queueName', nargs='*', default='all', dest='queues_list', help='queue name')
    args = parser.parse_args()
    if (args.mq_manager_name is None) or (args.queues_list is None) or (not args.queues_list):
        parser.print_usage()
        sys.exit(1)
    try:
        running_qmanagers = get_running_mq_manager(args.mq_manager_name)
        if not running_qmanagers:
            print('The running managers are missing.\nCheck managers status!')
            sys.exit(1)
        for qmanager in running_qmanagers:
            qs = get_not_empty_queues(args.queues_list, qmanager)
            for qgroup in qs:
                for item in qgroup:
                    clear_qlocal(item, qmanager)
                    print('The {} queue on the {} manager has been cleared'.format(item, qmanager))
        sys.exit(0)
    except Exception as error:
        print (error)
