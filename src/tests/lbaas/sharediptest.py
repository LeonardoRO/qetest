__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib

from qetest.src.tests.basetest import BaseTest

class SharedVirtualIPTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(SharedVirtualIPTest, self).__init__(all_loggers, conf)
        self.driver = driver

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(SharedVirtualIPTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def testSharedVirtualIp(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('SharedVirtualIPTest', retries,)

        #Call function to go to Load Balancers
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find the Load Balancers button',
                'FAILED - Load Balancers button click'):

                lbaaslib.go_to_lbaas(self.driver)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located Load Balancers button')
                self.logger.info('PASSED - Load Balancers button click')
                failed = False

        #Create 2 Load Balancers

        #Share IPs

        #Validation/Verification

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger, retrydict)
        return failed, totals