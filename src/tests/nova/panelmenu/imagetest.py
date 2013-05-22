# imagetest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import string

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelCreateImageTest(PanelBaseTest):
    """This class tests the panel menu power option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelCreateImageTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelCreateImageTest, self).setup(retries, testname)

    def testCreateImage(self, retries):
        """Tests for panel menu create image feature.

        NOTE: As of 15-Dec-2011 there is very little beyond the three steps being taken below to
        test Create Image.  There are currently no confirmations or notifications to the end
        user to use for validation.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 4,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testCreateImage', retries)

        # Click on the panel menu's rebuild option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the create image link',
                                        'FAILED - Create Image Option Test'):
                createpath = ('%sdiv[@class="panel-menuitem create_image-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, createpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located create image option for node %s' % testnode)
                self.logger.info('PASSED - Create Image Option Test')
                failed = False

        # Click on the panel menu's rebuild option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to input image name',
                                        'FAILED - Image Name Input Test'):

                rand1 = ''.join(random.sample(string.letters + string.digits, 16))
                image_name = 'myimage-%s' % rand1
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '%sinput[attribute::type="text"]' % pmn,
                                    'send_keys', image_name)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Able to input name "%s"' % image_name)
                self.logger.info('PASSED - Image Name Input Test')
                failed = False

        # Click on the panel menu's rebuild option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to click on the submit button',
                                        'FAILED - Create Image Submit Test'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '%sbutton[@class="input-panel-button"]' % pmn,
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Able to click on the submit button')
                self.logger.info('PASSED - Create Image Submit Test')
                failed = False


        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testCreateImage', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
