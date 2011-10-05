from TestContent import TestContent
from sysconfig import sys
import os
import logging.handlers
import ConfigParser
import unittest
import glob

def execute_directory(path, logger, config):
    listing = os.listdir(path)
    for infile in listing:
        fullpath = '%s\\%s' % (path, infile);
        if (os.path.isdir(fullpath)):
            execute_directory(fullpath, logger, config)
    suite = unittest.TestSuite()
    for infile in glob.glob('%s\\*.csv' % path):
        testCase = TestContent()
        testCase.logger = logger
        testCase.config = config
        testCase.file_path = infile
        suite.addTest(testCase);
    if (suite.countTestCases() > 0):
        logger.info('Running test suite: %s' % path)
        unittest.TextTestRunner(stream=handler.stream, descriptions=1, verbosity=2).run(suite)

path = 'c:\\selectica\\testcases'
config = ConfigParser.ConfigParser()
config.readfp(open('%s\\selenium.cfg' % path))
logger = logging.getLogger()
handler = logging.handlers.TimedRotatingFileHandler('%s\\selenium.log' % path, 'midnight')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.info('Start to run all test cases')
execute_directory(path, logger, config)		
logger.info('Finished running all test cases')
sys.exit()
