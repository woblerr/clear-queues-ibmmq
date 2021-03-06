import os
import sys
import unittest
from clear_queues_ibmmq import (
    dis_qm,
    dis_qlocal,
    clear_qlocal,
    clear_qlocal_qload,
    get_running_mq_manager,
    get_not_empty_queues,
    list_non_system_qs,
    run,
    print_msg
)
sys.path.append(os.getcwd())


class TestClearQueuesIbmmqUnittest(unittest.TestCase):
    test_qm = 'QM1'
    valid_code = 0

    def test_dis_qm(self):
        valid_result = 'QMNAME({0})                                               STATUS(Running)\n'.format(self.test_qm)
        invalid_result_1 = 'AMQ7048E: The queue manager name is either not valid or not known.\n'
        invalid_result_2 = 'AMQ8919E: There are no matching IBM MQ queue manager names.\n'
        self.assertEqual((valid_result, 0), dis_qm('all'))
        self.assertEqual((valid_result, 0), dis_qm(self.test_qm))
        self.assertEqual((valid_result, 0), dis_qm('QM?'))
        self.assertEqual((valid_result, 0), dis_qm('QM*'))
        self.assertEqual((valid_result, 0), dis_qm('QM*1'))
        (output, rcode) = dis_qm('QM')
        self.assertEqual(invalid_result_1, output)
        (output, rcode) = dis_qm('QM?1')
        self.assertEqual(invalid_result_2, output)


    def test_dis_qlocal(self):
        test_q = 'DEV.QUEUE.1'
        (output, rcode) = dis_qlocal(test_q, self.test_qm)
        self.assertIn('AMQ8409I: Display Queue details', output)
        self.assertIn(test_q, output)
        self.assertIn('CURDEPTH(1)', output)

    def test_clear_qlocal(self):
        test_q = 'DEV.QUEUE.3'
        (output, rcode) = clear_qlocal(test_q, self.test_qm)
        self.assertIn('AMQ8022', output)
        self.assertIn('queue cleared.', output)
        self.assertIn('No commands have a syntax error.', output)
        self.assertIn('All valid MQSC commands were processed.', output)

    def test_clear_qlocal_qload(self):
        test_q = 'DEV.QUEUE.2'
        (output, rcode) = clear_qlocal_qload(test_q, self.test_qm)
        self.assertIn('Messages:1', output)
        (output, rcode) = clear_qlocal_qload(test_q, self.test_qm)
        self.assertIn('Messages:0', output)

    def test_get_running_mq_manager(self):
        valid_result = [self.test_qm]
        invalid_result = []
        self.assertEqual(valid_result, get_running_mq_manager('all'))
        self.assertEqual(valid_result, get_running_mq_manager(self.test_qm))
        self.assertEqual(invalid_result, get_running_mq_manager('QM'))

    def test_get_not_empty_queues(self):
        valid_q = ['DEV.QUEUE.1', 'DEV.DEAD.LETTER.QUEUE']
        valid_r = [['DEV.QUEUE.1'], ['DEV.DEAD.LETTER.QUEUE']]
        valid_q_regexp = ['DEV.*']
        valid_r_regexp = [['DEV.DEAD.LETTER.QUEUE', 'DEV.QUEUE.1']]
        invalid_q = ['SYSTEM.AUTH.DATA.QUEUE']
        invalid_r = [[]]
        self.assertEqual(valid_r, get_not_empty_queues(valid_q, self.test_qm))
        self.assertEqual(valid_r_regexp, get_not_empty_queues(valid_q_regexp, self.test_qm))
        self.assertEqual(invalid_r, get_not_empty_queues(invalid_q, self.test_qm))

    def test_list_non_system_qs(self):
        valid_data = 'AMQ8409: Display Queue details.\n QUEUE(DEV.QUEUE.1) TYPE(QLOCAL)\n CURDEPTH(1) \n'
        valid_r = ['DEV.QUEUE.1']
        invalid_data = 'AMQ8409: Display Queue details.\n QUEUE(SYSTEM.AUTH.DATA.QUEUE) TYPE(QLOCAL)\n CURDEPTH(1) \n'
        invalid_r = []
        self.assertEqual(valid_r, list_non_system_qs(valid_data))
        self.assertEqual(invalid_r, list_non_system_qs(invalid_data))

    def test_print_msg(self):
        test_q = 'DEV.QUEUE.1'
        test_1_q = 'clear qlocal({0})\nAMQ8022I: IBM MQ queue cleared.'.format(test_q)
        test_1_r = 'Queue {0} on manager {1} has been cleared\n'.format(test_q, self.test_qm)
        test_2_q = 'clear qlocal({0})\nAMQ8148S: IBM MQ object in use.'.format(test_q)
        test_2_r = 'Queue {0} on manager {1} in use. Can not be cleared! Try to use --qload\n'.format(test_q, self.test_qm)
        test_3_q = 'clear qlocal({0})\nAMQ8147S: IBM MQ object {1} not found.'.format(test_q,test_q)
        test_3_r = 'IBM MQ object {0} not found.'.format(test_q)
        test_4_q = 'Test'
        test_4_r = 'Queue {0} on manager {1} has been cleared by qload utility\n'.format(test_q, self.test_qm)
        self.assertEqual(test_1_r, print_msg(test_1_q, self.valid_code, test_q, self.test_qm, False))
        self.assertEqual(test_2_r, print_msg(test_2_q, self.valid_code, test_q, self.test_qm, False))
        self.assertIn(test_3_r, print_msg(test_3_q, self.valid_code, test_q, self.test_qm, False))
        self.assertIn(test_4_r, print_msg(test_4_q, self.valid_code, test_q, self.test_qm, True))



class TestClearQueuesIbmmqIntegration(unittest.TestCase):
    bin_py = sys.executable
    test_qm = 'QM1'
    valid_code = 0

    def test_help(self):
        valid_r = 'usage: python clear_queues_ibmmq.py [-m qmgrName] [-q queueName [queueName ...]] --qload\n'
        command = '{0} clear_queues_ibmmq.py -m'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual(valid_r, output)
        command = '{0} clear_queues_ibmmq.py -q'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual(valid_r, output)
        command = '{0} clear_queues_ibmmq.py -m -q'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual(valid_r, output)
        command = '{0} clear_queues_ibmmq.py -m -q --qload'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual(valid_r, output)

    def test_args(self):
        valid_r = 'Queue DEV.DEAD.LETTER.QUEUE on manager {0} has been cleared\n\n'.format(self.test_qm)
        command = '{0} clear_queues_ibmmq.py -m {1} -q DEV.DEAD.LETTER.QUEUE'.format(self.bin_py, self.test_qm)
        (output, rcode) = run(command)
        self.assertEqual((valid_r,self.valid_code), (output, rcode))


    def test_system(self):
        valid_r = ''
        command = '{0} clear_queues_ibmmq.py -q SYSTEM.*'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual((valid_r,self.valid_code), (output, rcode))

    def test_args_all(self):
        valid_r = 'Queue DEV.QUEUE.1 on manager {0} has been cleared\n\n'.format(self.test_qm,self.test_qm)
        command = '{0} clear_queues_ibmmq.py'.format(self.bin_py)
        (output, rcode) = run(command)
        self.assertEqual((valid_r,self.valid_code), (output, rcode))
