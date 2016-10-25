import unittest, json, jsonpickle, sys
from RecordingClasses import Recording, Session, Util
from schedule_session import schedule_session
#from .NodeListener import remove_ids_atq as remove_jobids
from NodeListener import clear_atq

class TestScheduleSession(unittest.TestCase):
    def runTest(self):
        r = Recording(starttime='12/12/2050 2:24', recordpath='testnamedeleteme.sc16', frequency=2412e6, length=1)
        s = Session(startingpath='/tmp/scheduleTest/', rfsnids=[0], recordings=[r])
        returned = schedule_session(s)
        jobid = returned.recordings[0].uniques['jobId']
        self.assertIsNotNone(jobid)
        # This should be uncommented when merged with master branch for new version of removeJobIds
        #remove_jobids(json.dumps({ 'jobIds' : [ jobid ] }))
        # But for now...
        returned = json.loads(clear_atq())
        self.assertEqual(int(returned['cancelledJobIds'][0]), jobid)

class TestJSONEncoderDecoder(unittest.TestCase):
    def runTest(self):
        r = Recording(starttime='12/12/2050 2:24', recordpath='testnamedeleteme.sc16', frequency=2412e6, length=1)
        s = Session(startingpath='/tmp/scheduleTest/', rfsnids=[0], recordings=[r])
        dumped = Util.dumps(s)
        print(sys.modules)
        #print('DUMPED', repr(dumped))
        loaded = Util.loads(dumped)
        self.assertEqual(loaded, s)
        self.assertEqual(loaded.recordings[0].length, 1)

if __name__ == '__main__':
    unittest.main()
