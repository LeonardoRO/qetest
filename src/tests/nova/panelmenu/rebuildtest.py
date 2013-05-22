# rebuildtest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.oviewlib as oviewlib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelRebuildTest(PanelBaseTest):
    """This class tests the panel menu power option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelRebuildTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelRebuildTest, self).setup(retries, testname)

    def testRebuild(self, retries):
        """Tests for panel menu rebuild feature.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testRebuild', retries)

        # Click on the panel menu's rebuild option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the rebuild link',
                                        'FAILED - Panel Menu Rebuild Option Test'):
                rebuildpath = ('%sdiv[attribute::class="panel-menuitem rebuild-panel-'
                               'menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, rebuildpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located rebuild option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Rebuild Option Test')
                failed = False

        # Randomly pick an OS flavor
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to grab the list of OS flavors and select one',
                                        'FAILED - Rebuild Server OS Test'):
                os_flavor = oviewlib.add_server_os(self.driver) 
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Randomly selected "%s" for the server' % os_flavor)
                self.logger.info('PASSED - Rebuild Server OS Test')
                failed = False

        # Submit the change by clicking on 'Rebuild Server' button
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to click on the Rebuild Server submit button',
                                        'FAILED - Rebuild Server Submit Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[@class="rebuild_button"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on the Rebuild Server button to submit')
                self.logger.info('PASSED - Rebuild Server Submit Test')
                failed = False

        # Click on the OK in the pop-up confirmation dialog
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to click on the OK button in the confirmation box',
                                        'FAILED - Rebuild Server Submit Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, '//button[@name="ok"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on the OK button in the confirmation box')
                self.logger.info('PASSED - Rebuild Server Submit Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testRebuild', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals
