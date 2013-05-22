__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib

from qetest.src.tests.basetest import BaseTest

class RenameTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(RenameTest, self).__init__(all_loggers, conf)
        self.driver = driver

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(RenameTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def testRename(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('RenameTest', retries,)

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

        #Rename a Load Balancer (From Detail Page)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to rename a random Load Balancer',
                'FAILED - Random Load Balancer Rename'):

                #Click the name to enable editing
                path = '//div[@id="node_header"]/descendant::div[@class="node_name"]/div/div'
                sellib.element_wait(self.driver.find_element_by_xpath, path, element_action='click')

                #Insert new name
                path = '//div[@id="node_header"]/descendant::div[@class="node_name"]/div/input'
                name = lbaaslib.get_random_name()
                sellib.element_wait(self.driver.find_element_by_xpath, path, element_action='clear')
                sellib.element_wait(self.driver.find_element_by_xpath, path, element_action='send_keys', action_arg=name)

                #Get back to load balancers list and click the renamed load balancer
                lbaaslib.go_to_lbaas(self.driver)
                lbaaslib.click_load_balancer_by_name(self.driver, name)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Random Load Balancer Renamed')
                self.logger.info('PASSED - Load Balancer Rename')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger, retrydict)
        return failed, totals
