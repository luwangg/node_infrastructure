import unittest, json, jsonpickle, sys
from nodelistener import *
#from recording_classes import Recording, Session, Util
from nodelistener.schedule_session import schedule_session
from nodelistener.nodelistener import clear_atq, filedrop
import platform

class TestScheduleSession(unittest.TestCase):

    def runTest(self):
        if platform.system() != 'Linux':
            return 
        r = Recording(starttime='12/12/2050 2:24', recordpath='testnamedeleteme.sc16', frequency=2412e6, length=1)
        s = Session(startingpath='/tmp/scheduleTest/', rfsnids=[0], recordings=[r])
        returned = schedule_session(s)
        jobid = returned.recordings[0].uniques['jobId']
        self.assertIsNotNone(jobid)
        returned = json.loads(clear_atq())
        self.assertEqual(int(returned['cancelledJobIds'][0]), jobid)

class TestJSONEncoderDecoder(unittest.TestCase):
    def runTest(self):
        if platform.system() != 'Linux':
            return
        r = Recording(starttime='12/12/2050 2:24', recordpath='testnamedeleteme.sc16', frequency=2412e6, length=1)
        s = Session(startingpath='/tmp/scheduleTest/', rfsnids=[0], recordings=[r])
        dumped = Util.dumps(s)
        loaded = Util.loads(dumped)
        self.assertEqual(loaded, s)
        self.assertEqual(loaded.recordings[0].length, 1)

''' Fails but doesn't throw error!
class TestFiledropSession(unittest.TestCase):
    def runTest(self):
        passing = {'spath': '/home/ops/testfolder/', 'rfsnid':'1',
                'fpath':'test', 'date':'20161029', 'game':'duke',
                'scheduletime': '2:30 PM 11/15/2016'}
        print(filedrop(json.dumps(passing)))
'''

if __name__ == '__main__':
    unittest.main()
