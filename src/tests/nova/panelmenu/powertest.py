# powertest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelPowerTest(PanelBaseTest):
    """This class tests the panel menu power option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelPowerTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries, findnode=True):
        return super(PanelPowerTest, self).setup(retries, testname, findnode)

    def testReboot(self, retries):
        """Test panel menu power reboot functionality.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 4,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testReboot', retries)

        # Click on the panel menu's power option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the power option',
                                        'FAILED - Panel Menu Power Option Test'):
                powerpath = ('%sdiv[attribute::class="panel-menuitem power-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, powerpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located power option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Power Option Test')
                failed = False

        # Click on the reboot option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the reboot button',
                                        'FAILED - Power Reboot Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::class="soft_reboot_button"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath, 
                                    '//button[attribute::name="ok"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Rebooted node %s' % testnode)
                self.logger.info('PASSED - Power Reboot Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testReboot', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testHardReboot(self, retries):
        """Test panel menu power hard reboot functionality.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 4,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testHardReboot', retries)

        # Click on the panel menu's power option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the power option',
                                        'FAILED - Panel Menu Power Option Test'):
                powerpath = ('%sdiv[attribute::class="panel-menuitem power-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, powerpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located power option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Power Option Test')
                failed = False

        # Click on the hard reboot option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the hard reboot button',
                                        'FAILED - Power Hard Reboot Test'):
                hr_button_path = '//button[attribute::class="hard_reboot_button"]'
                sellib.element_wait(self.driver.find_element_by_xpath, hr_button_path, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::name="ok"]', 
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Hard rebooted node %s' % testnode)
                self.logger.info('PASSED - Power Reboot Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testHardReboot', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testDestroy(self, retries):
        """Test panel menu power destroy functionality.

        NOTE: This is left in here and does not use the oviewlib.delete_node functionality because
        it is being called out as it's own explicit test.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 3,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testDestroy', retries)
        
        # Click on the panel menu's power option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the power option',
                                        'FAILED - Panel Menu Power Option Test'):
                powerpath = ('%sdiv[attribute::class="panel-menuitem power-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, powerpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located power option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Power Option Test')
                failed = False

        # Click on the destroy option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the destroy button',
                                        'FAILED - Destroy Server Node Test'):
                self.driver.find_element_by_xpath('//button[attribute::class='
                                                  '"destroy_button"]').click()
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::name="ok"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked the "OK" button for node %s' % testnode)
                self.logger.info('PASSED - Destroy Server Node Test')
                failed = False

        # NOTE: This doesn't mean that it actually worked, just that Reach
        # tried to destroy the node.  There doesn't currently seem to be a
        # growl-ish confirmation message.

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testDestroy', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals

    def testCancelReboot(self, retries):
        """Tests panel menu power cancel then reboot functionality.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 3,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testCancelReboot', retries)

        # Click on the panel menu's power option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the power option',
                                        'FAILED - Panel Menu Power Option Test'):
                powerpath = ('%sdiv[attribute::class="panel-menuitem power-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, powerpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located power option for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Power Option Test')
                failed = False

        # Validate the 'cancel' functionality
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Cancel then reboot doesn\'t appear to be working',
                                        'FAILED - Power Panel Cancel Link Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::class="soft_reboot_button"]', 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::name="cancel"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on reboot then on cancel in the confirmation pop-up')
                try:
                    sellib.element_wait(self.driver.find_element_by_xpath,
                                        '//div[attribute::class="ck_widgets_message_default" and '
                                        'contains(text(), "Rebooting %s")]' % testnode)
                    temp_failed = True
                    self.logger.error('Reboot confirm message found, indicating cancel failure')
                except Exception:
                    self.logger.debug('After clicking cancel, no reboot confirmation seen')
                    temp_failed = False
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::class="soft_reboot_button"]', 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::name="ok"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on reboot again, and on ok (in the confirmation pop-up)')
                self.logger.debug('Cancel button seems to be working %s' % testnode)
                self.logger.info('PASSED - Power Panel Cancel Link Test')
                if not temp_failed:
                    failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testCancelReboot', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
