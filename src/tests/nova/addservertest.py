# addservertest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import time

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.oviewlib as oviewlib

from qetest.src.tests.basetest import BaseTest


class AddServerTest(BaseTest):
    """This class tests the overview page's batch operations"""

    def __init__(self, all_loggers, conf, driver):
        super(AddServerTest, self).__init__(all_loggers, conf)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(AddServerTest, self).setup(retries, testname)
        failed = oviewlib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        return starttime, retrydict, failed
    
    def testAddServer(self, retries):
        
        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('testAddServer', retries,)

        # Click on the top Add Server button
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to find the top "Add Server" button',
                                        'FAILED - Add Server Top Button Test'):
                oviewlib.add_server_button_top(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the top "Add Server" button')
                self.logger.info('PASSED - Add Server Top Button Test')
                failed = False

        # Input a server name
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to add the server name',
                                        'FAILED - Add Server Name Test'):
                server_name = oviewlib.add_server_name(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Added the server name "%s"' % server_name)
                self.logger.info('PASSED - Add Server Name Test')
                failed = False

        # Randomly pick an OS
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to grab the list of OS flavors and select one',
                                        'FAILED - Add Server OS Test'):
                os_flavor = oviewlib.add_server_os(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Randomly selected "%s" for the server' % os_flavor)
                self.logger.info('PASSED - Add Server OS Test')
                failed = False

        # Randomly choose a size
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to grab the list of server sizes and select one,',
                                        'FAILED - Add Server Size Test'):
                server_size = oviewlib.add_server_size(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Randomly selected "%s" as the server size' % server_size)
                self.logger.info('PASSED - Add Server Size Test')
                failed = False

        # Click on the bottom Add Server to submit it
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to find the bottom "Add Server" button',
                                        'FAILED - Add Server Submit Test'):
                oviewlib.add_server_button_bottom(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the bottom "Add Server" button')
                self.logger.info('PASSED - Add Server Submit Test')
                failed = False

        # Look for a "server being created" growl notification
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Didn\'t see a server creation confirmation',
                                        'FAILED - Add Server Confirmation Test'):
                path = ('//div[@class="ck_widgets_message_default" and contains(text(), '
                        '"Server %s is being created")]' % server_name)
                sellib.element_wait(self.driver.find_element_by_xpath, path)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found a growl "create" confirmation message')
                self.logger.info('PASSED - Add Server Confirmation Test')
                failed = False

        # Do a check for servers created from previous tests and delete them
        # TODO: Need to move this out from here, into it's own module and have
        #       the test manager call it.
#        with sellib.error_handler(self.driver, self.all_loggers, retrydict,
#                                        'There was an issue removing previous, session specific '
#                                        'nodes'):
#            oviewlib.overview_reset(self.driver, self.all_loggers, retrydict, self.sleepdict)
#            nodeid_list = oviewlib.get_nodeid_list(self.driver)
#            server_name_list = oviewlib.get_server_name_list()
#            for item in nodeid_list:
#                nodename = oviewlib.get_nodename(self.driver, item)
#                for server_name in server_name_list:
#                    if server_name == nodename[:len(server_name)]:
#                        self.driver.refresh()
#                        time.sleep(10)
#                        oviewlib.delete_node(self.driver, item, self.sleepdict)
#                        sellib.sleeper(self.sleepdict)
#                        self.logger.debug('Server "%s" deleted' % nodename)

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testAddServer', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
