__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import re

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.lbaaslib as lbaaslib
import qetest.src.libs.humansortlib as humansortlib

from qetest.src.tests.basetest import BaseTest
from qetest.src.libs.exceptlib import ListOrderComparisonError

class ListViewTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(ListViewTest, self).__init__(all_loggers, conf)
        self.driver = driver
        self.initial_elements_list = []
        self.initial_protocolports_elements_list = []

    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(ListViewTest, self).setup(retries, testname)
        failed = lbaaslib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed

    def get_protocolports(self):

        protocolportspath = ('//div[@class="data_table_body"]/descendant::div[@class="data_table_cell protocol_port"]')

        return sellib.elements_wait(self.driver, protocolportspath)

    def get_loadbalancer_list(self):

        path = ('//div[@class="data_table_body"]/descendant::div[@class="data_table_cell name"]')

        return sellib.elements_wait(self.driver, path)

    def sortable_int(self, value):
        return int(re.sub(r'\$?([0-9]*).*', '\\1', str(value)))

    def compare_sorting(self, list1, list2):
        if len(list1) != len(list2):
            raise ListOrderComparisonError(list1, list2)

        for x in range(len(list1)):
            if list1[x] != list2[x]:
                raise ListOrderComparisonError(list1, list2)

    def testListView(self, retries):

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('ListViewTest', retries,)

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

        # Get the initial load balancers lists
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find or gather the load balancers',
                'FAILED - Gather Load Balancers Test'):

                initial_name_list = self.get_loadbalancer_list() #list of objects

                self.initial_elements_list = [name.text.lower() for name in initial_name_list]

                sellib.sleeper(self.sleepdict)
                self.logger.info('PASSED - Gather Load Balancers Test')
                failed = False

        #Compare list sorted by Name (Ascending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed comparison of sorted names list (ascending)',
                'FAILED - Sort by Name Test (ascending)'):

                ascending_elements = self.get_loadbalancer_list()
                ascending_name_list = [name.text.lower() for name in ascending_elements]

                self.compare_sorting(ascending_name_list, sorted(self.initial_elements_list))

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Names list assorted correctly (ascending)')
                self.logger.info('PASSED - Sort by Name Test (ascending)')
                failed = False

        #Sort by Name (Descending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed to find the name header (descending)',
                'FAILED - Sort by Name Test (descending)'):

                lbaaslib.sort_by_name_desc(self.driver)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the name header (descending)')
                self.logger.info('PASSED - Sort by Name Test (descending)')
                failed = False

        #Compare list sorted by Name (Descending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed comparison of sorted names list (descending)',
                'FAILED - Sort by Name Test (descending)'):

                descending_elements = self.get_loadbalancer_list()
                descending_name_list = [name.text.lower() for name in descending_elements]

                self.compare_sorting(descending_name_list, sorted(self.initial_elements_list, reverse=True))

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Names list assorted correctly (descending)')
                self.logger.info('PASSED - Sort by Name Test (descending)')
                failed = False

        # Get the initial protocol/ports list
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Unable to find or gather the protocol/ports',
                'FAILED - Gather Protocol/Port Test'):

                initial_protocolport_list = self.get_protocolports() #list of objects
                self.initial_protocolports_elements_list = [name.text.lower() for name in initial_protocolport_list]

                sellib.sleeper(self.sleepdict)
                self.logger.info('PASSED - Gather Protocol/Port Test')
                failed = False

        #Sort by Protocol/Port (Ascending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed to find the protocol/port header (ascending)',
                'FAILED - Sort by Protocol/Port Test (ascending)'):

                lbaaslib.sort_by_protocol_port_asc(self.driver)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the protocol/port header (ascending)')
                self.logger.info('PASSED - Sort by Protocol/Port Test (ascending)')
                failed = False

        #Compare list sorted by Protocol/Port (Ascending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed comparison of sorted protocol/ports list (ascending)',
                'FAILED - Sort by Protocol/Port Test (ascending)'):

                ascending_protocolport_elements = self.get_protocolports()
                ascending_protocolport_list = [name.text.lower() for name in ascending_protocolport_elements]

                humansorted_list = humansortlib.sort_nicely(self.initial_protocolports_elements_list)
                self.compare_sorting(ascending_protocolport_list, humansorted_list)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Protocol/Port list assorted correctly (ascending)')
                self.logger.info('PASSED - Sort by Protocol/Port Test (ascending)')
                failed = False

        #Sort by Protocol/Port (Descending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed to find the protocol/port header (descending)',
                'FAILED - Sort by Protocol/Port Test (descending)'):

                lbaaslib.sort_by_protocol_port_desc(self.driver)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the protocol/port header (descending)')
                self.logger.info('PASSED - Sort by Protocol/Port Test (descending)')
                failed = False

        #Compare list sorted by Protocol/Port (Descending)
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                'Failed comparison of sorted protocol/ports list (descending)',
                'FAILED - Sort by Protocol/Port Test (descending)'):

                descending_protocolport_elements = self.get_protocolports()
                descending_protocolport_list = [name.text.lower() for name in descending_protocolport_elements]

                humansorted_list = humansortlib.sort_nicely_reverse(self.initial_protocolports_elements_list)
                self.compare_sorting(descending_protocolport_list, humansorted_list)

                sellib.sleeper(self.sleepdict)
                self.logger.debug('Protocol/Port list assorted correctly (descending)')
                self.logger.info('PASSED - Sort by Protocol/Port Test (descending)')
                failed = False

        #TODO: Sort by Node

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testListView', totals, failed, starttime, self.logger,
        retrydict)
        return failed, totals