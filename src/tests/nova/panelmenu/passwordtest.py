# passwordtest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelPasswordTest(PanelBaseTest):
    """This class tests the panel menu password option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelPasswordTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelPasswordTest, self).setup(retries, testname)

    def testResetPassword(self, retries):
        """Tests for panel menu password reset feature.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """
        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testResetPassword', retries)

        # Click on the panel menu's reset password option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the reset password link',
                                        'FAILED - Panel Menu Reset Password Option Test'):
                resetpath = ('%sdiv[attribute::class="panel-menuitem password-panel-'
                             'menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, resetpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located reset password option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Reset Password Option Test')
                failed = False

        # Click on the 'Reset root password' button
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the \'Reset root password\' button',
                                        'FAILED - Reset Password Button Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::class="reset_root_button"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found and clicked on the \'Reset root password\' button')
                self.logger.info('PASSED - Reset Password Button Test')
                failed = False

        # Click on the 'Show password' button
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Show password is working incorrectly or not clickable',
                                        'FAILED - Show Password Button Test'):
                # Is it hidden?
                sellib.element_wait(self.driver.find_element_by_xpath,
                                     '//input[@class="display_password" and @type="password"]')
                # Click on the button to show it
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[@class="show_password"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Show password is working correctly and is clickable')
                self.logger.info('PASSED - Show Password Button Test')
                failed = False

        # Click on the 'Hide password' button
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Hide password is working incorrectly or not clickable',
                                        'FAILED - Hide Password Button Test'):
                # Is is displayed?
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//input[@class="display_password" and @type="input"]')
                # Click on the button to hide it
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[@class="hide_password"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Hide password is working correctly and is clickable')
                self.logger.info('PASSED - Hide Password Button Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testResetPassword', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
