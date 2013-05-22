__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib

from qetest.src.tests.basetest import BaseTest

class DetailViewTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(DetailViewTest, self).__init__(all_loggers, conf)
        self.driver = driver

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(DetailViewTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def testDetailView(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('DetailViewTest', retries,)

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

        #Check if Load Balancer Details section exist
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find Load Balancer Details section',
                'FAILED - Find Load Balancer Details Section'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="content"]/div[@id="node_details"]')

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Load Balancer Details Section Found')
                self.logger.info('PASSED - Find Load Balancer Details Section')
                failed = False

        #Check if Nodes section exist
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find nodes section',
                'FAILED - Find Nodes Section'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="content"]/div[@id="node_servers"]')

        sellib.sleeper(self.sleepdict)
        self.logger.debug('Nodes Section Found')
        self.logger.info('PASSED - Find Nodes Section')
        failed = False

        #Check if Optional Features section exist
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find Optional Features section',
                'FAILED - Find Optional Features Section'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="content"]/div[@id="node_options"]')

        sellib.sleeper(self.sleepdict)
        self.logger.debug('Optional Features Section Found')
        self.logger.info('PASSED - Find Optional Features Section')
        failed = False

        #Protocol/Port
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to open the Protocol/Port popup',
                'FAILED - Protocol/Port Popup Test'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="node_details"]/descendant::a[@id="protocol_port_toggle"]', element_action='click')
                sellib.sleeper(self.sleepdict)

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//form[@class="protocol-port"]/div[@class="save-cancel"]/button[@class="button-cancel"]',
                    element_action='click')

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Protocol/Port popup test passed')
                self.logger.info('PASSED - Protocol/Port Popup Test')
                failed = False

        #Algorithm
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to open the Algorithm popup',
                'FAILED - Algorithm Popup Test'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="node_details"]/descendant::a[@id="algorithm_toggle"]', element_action='click')
                sellib.sleeper(self.sleepdict)

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//form[@class="load-balancer-algorithm"]/div[@class="save-cancel"]/button[@class="button-cancel"]',
                    element_action='click')

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Algorithm Popup Test Passed')
                self.logger.info('PASSED - Algorithm Popup Test')
                failed = False

    #Nodes
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find a Node on the table',
                'FAILED - Node not found'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="node_servers"]/div[@id="node_list"]/div[@class="data_table"]/div[@class="data_table_body"]/div[@class="data_table_row"][1]/div[@class="data_table_cell name"]')

            sellib.sleeper(self.sleepdict)
            self.logger.debug('Find a Node on the Table')
            self.logger.info('PASSED - node Found')
            failed = False

##Optional Features #TODO: make it random
        #Health Monitoring
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to open the Health Monitoring popup',
                'FAILED - Health Monitoring Test'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@id="node_options"]/descendant::a[@id="health_monitor_toggle"]', element_action='click')

                sellib.element_wait(self.driver.find_element_by_xpath,
                    '//div[@class="health_monitor"]/div[@class="save-cancel"]/a[@class="cancel"]',
                    element_action='click')

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Health Monitoring Test Passed')
                self.logger.info('PASSED - Health Monitoring Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger, retrydict)
        return failed, totals