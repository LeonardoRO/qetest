# panelbasetest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random

import qetest.src.libs.oviewlib as oviewlib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.basetest import BaseTest

class PanelBaseTest(BaseTest):

    def __init__(self, all_loggers, conf, driver):
        super(PanelBaseTest, self).__init__(all_loggers, conf)
        self.driver = driver
        
    def setup(self, retries, testname, findnode=True):
        pmn = None
        nodename = None
        logger = self.all_loggers[0]
        (starttime, retrydict) = super(PanelBaseTest, self).setup(retries, testname)
        failed = oviewlib.setup(self.driver, self.all_loggers, retrydict, self.conf.sleepdict)
        if findnode:
            if not failed:
                (nodeid, nodename, failed) = self.get_random_node(retrydict)
            if not failed:
                pmn = oviewlib.get_pmn(nodeid)
                with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                 'Unable to find sprocket for nodename "%s"' % nodename,
                                 'FAILED - Sprocket Location Test'):
                    failed = oviewlib.find_sprocket(self.driver, nodeid)
                    logger.debug('Found sprocket for node "%s"' % nodename)
                    logger.info('PASSED - Sprocket Location Test')
                    failed = False
        
        return (starttime, retrydict, failed, pmn, nodename)

    def get_nodeid_list(self):
        node_elements = sellib.elements_wait(self.driver, '//div[@class="node"]')
        nodeid_list = [element.get_attribute('data-node_id') for element in node_elements]

        return nodeid_list

    def get_nodename(self, nodeid):
        namepath = ('//div[@class="node" and @data-node_id="%s"]/descendant::div[@class='
                    '"goog-control ck_widgets_glance_name"]' % nodeid)
        myelement = sellib.element_wait(self.driver.find_element_by_xpath, namepath)
        nodename = myelement.text

        return nodename

    def get_random_node(self, retrydict):
        failed = True
        nodeid = None
        nodename = None
        with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                           'No nodes are being displayed',
                           'FAILED - Node List Display Test'):
            nodeid_list = self.get_nodeid_list()
            nodeid = random.choice(nodeid_list)
            sellib.sleeper(self.conf.sleepdict)
            self.logger.debug('Node list created')
            self.logger.info('PASSED - Node List Display Test')
            failed = False

        if not failed:
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                              'Unable to determine node name from nodeid',
                               'FAILED - Node Name Discovery Test'):
                nodename = self.get_nodename(nodeid)
                sellib.sleeper(self.conf.sleepdict)
                self.logger.debug('Node name found')
                self.logger.info('PASSED - Node Name Discovery Test')
                failed = False

        return nodeid, nodename, failed
