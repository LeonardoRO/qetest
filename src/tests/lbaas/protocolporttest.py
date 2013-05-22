__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib

from qetest.src.tests.basetest import BaseTest

class ProtocolPortTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(ProtocolPortTest, self).__init__(all_loggers, conf)
        self.driver = driver

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(ProtocolPortTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def testProtocolPort(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('ProtocolPortTest', retries,)

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

        #Call function to click on a random Load Balancer
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to select a random Load Balancer',
                'FAILED - Random Load Balancer selection'):

                lbaaslib.random_load_balancer(self.driver)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Random Load Balancer Selected')
                self.logger.info('PASSED - Random Load Balancer selection')
                failed = False

        #Protocol/Port
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to select a random Load Balancer',
                'FAILED - Random Load Balancer selection'):

                #TODO: add tests on the popup (change protocol/port and save)
                #string
                #special chars
                #script
                #0.5
                #5.5
                #5.5.5
                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="node_details"]/descendant::a[@id="protocol_port_toggle"]', element_action='click')

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Random Load Balancer Selected')
                self.logger.info('PASSED - Random Load Balancer selection')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger, retrydict)
        return failed, totals