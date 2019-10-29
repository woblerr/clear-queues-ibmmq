import os
import sys
import unittest
from clear_queues_ibmmq import *
sys.path.append(os.getcwd())



class TestClearQueuesIbmmqUnittest(unittest.TestCase):
    test_qm = 'QM1'

    def test_dis_qm(self):
        valid_result = 'QMNAME({})                                               STATUS(Running)\n'.format(self.test_qm)
        invalid_result_1 = 'AMQ7048E: The queue manager name is either not valid or not known.\n'
        invalid_result_2 = 'AMQ8919E: There are no matching IBM MQ queue manager names.\n'
        self.assertEqual(valid_result, dis_qm('all'))
        self.assertEqual(valid_result, dis_qm(self.test_qm))
        self.assertEqual(valid_result, dis_qm('QM?'))
        self.assertEqual(valid_result, dis_qm('QM*'))
        self.assertEqual(valid_result, dis_qm('QM*1'))
        self.assertEqual(invalid_result_1, dis_qm('QM'))
        self.assertEqual(invalid_result_2, dis_qm('QM?1'))

    def test_dis_qlocal(self):
        test_q = 'DEV.QUEUE.1'
        output = dis_qlocal(test_q, self.test_qm)
        self.assertIn('AMQ8409I: Display Queue details', output)
        self.assertIn(test_q, output)
        self.assertIn('CURDEPTH(1)', output)

    def test_clear_qlocal(self):
        test_q = 'DEV.QUEUE.3'
        output = clear_qlocal(test_q, self.test_qm)
        self.assertIn('AMQ8022I: IBM MQ queue cleared.', output)
        self.assertIn('No commands have a syntax error.', output)
        self.assertIn('All valid MQSC commands were processed.', output)

    def test_get_running_mq_manager(self):
        valid_result = [self.test_qm]
        invalid_result = []
        self.assertEqual(valid_result, get_running_mq_manager('all'))
        self.assertEqual(valid_result, get_running_mq_manager(self.test_qm))
        self.assertEqual(invalid_result, get_running_mq_manager('QM'))

    def test_get_not_empty_queues(self):
        valid_q = ['DEV.QUEUE.1', 'DEV.QUEUE.2']
        valid_r = [['DEV.QUEUE.1'], ['DEV.QUEUE.2']]
        valid_q_regexp = ['DEV.*']
        valid_r_regexp = [['DEV.DEAD.LETTER.QUEUE', 'DEV.QUEUE.1', 'DEV.QUEUE.2']]
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


class TestClearQueuesIbmmqIntegration(unittest.TestCase):
    bin_py = sys.executable
    test_qm = 'QM1'

    def test_help(self):
        valid_r = 'usage: python clear_queues_ibmmq.py [-m qmgrName] [-q queueName [queueName ...]]\n'
        command = '{} clear_queues_ibmmq.py -m'.format(self.bin_py)
        self.assertEqual(valid_r, run(command))
        command = '{} clear_queues_ibmmq.py -q'.format(self.bin_py)
        self.assertEqual(valid_r, run(command))
        command = '{} clear_queues_ibmmq.py -m -q'.format(self.bin_py)
        self.assertEqual(valid_r, run(command))

    def test_args(self):
        valid_r = 'The DEV.DEAD.LETTER.QUEUE queue on the {} manager has been cleared\n'.format(self.test_qm)
        command = '{} clear_queues_ibmmq.py -m {} -q DEV.DEAD.LETTER.QUEUE'.format(self.bin_py, self.test_qm)
        self.assertEqual(valid_r, run(command))

    def test_system_1(self):
        valid_r = ''
        command = '{} clear_queues_ibmmq.py -q SYSTEM.*'.format(self.bin_py)
        self.assertEqual(valid_r, run(command))

    def test_args_all(self):
        valid_r = 'The DEV.QUEUE.1 queue on the {} manager has been cleared\nThe DEV.QUEUE.2 queue on the {} manager has been cleared\n'.format(self.test_qm, self.test_qm)
        command = '{} clear_queues_ibmmq.py'.format(self.bin_py)
        self.assertEqual(valid_r, run(command))
