__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib

from qetest.src.tests.basetest import BaseTest
#from qetest.src.libs.exceptlib import TextNotFoundError as texterror

class AlgorithmTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(AlgorithmTest, self).__init__(all_loggers, conf)
        self.driver = driver

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(AlgorithmTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def click_algorithm_by_name(self, algorithm_name):
        path = ('//div[contains(text(), "%s")]' % algorithm_name)
        sellib.element_wait(self.driver.find_element_by_xpath, path, element_action='click')

    #TODO: check name
    def get_algorithm_name_details_view(self):
        path = ('//div[@id="node_details"]/div/dl/dt[3]')
        existing_algorithm_name_details_view = sellib.elements_wait(self.driver, path)
        existing_algorithm_name_details_view_text = [name.text for name in existing_algorithm_name_details_view]
        print('this is the existing_algorithm_name_details_view_text: ')
        print existing_algorithm_name_details_view_text
        return existing_algorithm_name_details_view_text

    def algorithm_select(self, name):
        temp_failed = True

        #Open Algorithm popup
        sellib.element_wait(self.driver.find_element_by_xpath,
            '//div[@id="node_details"]/descendant::a[@id="algorithm_toggle"]', element_action='click')
        sellib.sleeper(self.sleepdict)

        #Select Algorithm
        self.click_algorithm_by_name(name)
        sellib.sleeper(self.sleepdict)

        #Save
        sellib.element_wait(self.driver.find_element_by_xpath,
            '//div[@class="ck-widgets-popup ck-widgets-popup-right"][2]/div[@class="ck-widgets-popup-content"]/form[@class="load-balancer-algorithm"]/div[@class="save-cancel"]/button[@class="button-save"]',
            element_action='click')
        sellib.sleeper(self.sleepdict)

#        #Grab Algorithm name @ details view
#        grabbed_text = self.get_algorithm_name_details_view()
#        print ('-----------------------------')
#        print grabbed_text
#        print ('-----------------------------')
#        if grabbed_text == name:
#            temp_failed = False
#
#        return temp_failed

    def testAlgorithm(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('DetailViewTest', retries,)

        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find the Load Balancers button',
                'FAILED - Load Balancers button click'):

                    #lbaaslib.go_to_lbaas(self.driver)
                    self.driver.get("https://privatebeta.rackspace.com/a/reachdevsf/load_balancers")

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

#        #Algorithm Cancel
#        if not failed:
#            totals.update(executed = totals['executed'] + 1)
#            failed = True
#            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
#                'Unable to open the Algorithm popup',
#                'FAILED - Algorithm Popup Test'):
#
#                sellib.element_wait(self.driver.find_element_by_xpath,
#                    '//div[@id="node_details"]/descendant::a[@id="algorithm_toggle"]', element_action='click')
#
#                sellib.element_wait(self.driver.find_element_by_xpath,
#                    '//div[@class="ck-widgets-popup ck-widgets-popup-right"][2]/div[@class="ck-widgets-popup-content"]/form[@class="load-balancer-algorithm"]/div[@class="save-cancel"]/button[@class="button-cancel"]',
#                    element_action='click')
#
#                sellib.sleeper(self.sleepdict)
#                self.logger.debug('Algorithm Popup Test Passed')
#                self.logger.info('PASSED - Algorithm Popup Test')
#                failed = False

        #Select Algorithm
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to open the Algorithm popup',
                'FAILED - Algorithm Popup Test'):

                algorithm_list = ['Round Robin', 'Weighted Round Robin', 'Random', 'Least Connections', 'Weighted Least Connections']
                for name in algorithm_list:
                    self.algorithm_select(name)
                    current_name = self.get_algorithm_name_details_view()
                    if current_name != name:
                        print name
                        print current_name
                        print ('its different!')
                    else:
                        sellib.sleeper(self.sleepdict)
                        self.logger.debug('Algorithm Popup Test Passed')
                        self.logger.info('PASSED - Algorithm Popup Test')
                        failed = False

#                #TODO: get list from screen
#                algorithm_list = ['Round Robin', 'Weighted Round Robin', 'Random', 'Least Connections', 'Weighted Least Connections']
#                for name in algorithm_list:
#                    current_name = self.get_algorithm_name_details_view()
#                    if current_name != name:
#                        temp_failed = self.algorithm_select(name)
#                        if temp_failed:
#                            break
#            if temp_failed:
#                raise texterror
#            else:
#                sellib.sleeper(self.sleepdict)
#                self.logger.debug('Algorithm Popup Test Passed')
#                self.logger.info('PASSED - Algorithm Popup Test')
#                failed = False

#
##        close algorithm popup
##        sellib.element_wait(self.driver.find_element_by_xpath,
##            '//div[@class="ck-widgets-popup ck-widgets-popup-right"][2]/div[@class="ck-widgets-popup-content"]/form[@class="load-balancer-algorithm"]/div[@class="save-cancel"]/button[@class="button-cancel"]',
##            element_action='click')

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger, retrydict)
        return failed, totals