# basetest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import time

class BaseTest(object):

    def __init__(self, all_loggers, conf):
        self.logger = all_loggers[0]
        self.trace_logger = all_loggers[1]
        self.all_loggers = all_loggers
        self.conf = conf
        self.opts = conf.opts
        self.testurl = conf.testurl
        self.keys = conf.keys
        self.uname = conf.opts.dataset
        self.pword = conf.opts.dataset
        self.dataset = conf.opts.dataset
        self.sleepdict = conf.sleepdict
        
    def setup(self, retries, test_name):
        if retries < 1:
            self.logger.info('Start ==> %s' % test_name)
        else:
            self.logger.info('Start ==> %s (Retry: %s)' % (test_name, retries))
        starttime = round(time.time() * 1000)
        retrydict = dict(retries=retries, max_retries=self.opts.retry)

        return starttime, retrydict
