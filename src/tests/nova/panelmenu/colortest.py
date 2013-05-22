# colortest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.oviewlib as oviewlib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelColorTest(PanelBaseTest):
    """This class tests the panel menu color option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelColorTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelColorTest, self).setup(retries, testname)

    def testPanelMenuColors(self, retries):
        """Tests for changing individual node's background color.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testPanelMenuColors', retries)

        colors = oviewlib.panel_colors()
        total_colors = len(colors)

        # Click on the panel menu's color option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the color panel',
                                        'FAILED - Panel Menu Color Option Test'):
                colorpanelpath = ('%sdiv[attribute::class="panel-menuitem '
                                  'color-panel-menuitem"]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, colorpanelpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located color panel for node %s' % testnode)
                self.logger.info('PASSED - Panel Menu Color Option Test')
                failed = False

        # Click on a few random colors then set it back to white
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            rand1 = random.randint(0, total_colors - 2)
            rand2 = rand1
            while rand2 == rand1:
                rand2 = random.randint(0, total_colors - 2)
            random_colors = (colors[rand1], colors[rand2], colors[total_colors - 1])
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to randomly set some colors',
                                        'FAILED - Panel Menu Color Selection Test'):
                for kolor in random_colors:
                    colorpath = ('%sdiv[attribute::title="RGB %s"]' % (pmn, kolor))
                    sellib.element_wait(self.driver.find_element_by_xpath, colorpath, 'click')
                    sellib.sleeper(self.sleepdict)
                self.logger.debug('Random color change succeeded')
                self.logger.info('PASSED - Panel Menu Color Selection Test')
                failed = False

        # Test the 'custom colors' input box and close the panel menu
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to set a custom color',
                                        'FAILED - Node Custom Color Test'):
                colorpath = ('%sinput[attribute::class="label-input-label"]' % pmn)
                oviewlib.custom_colors(self.driver, self.logger, colorpath, self.sleepdict)
                self.logger.info('PASSED - Node Custom Color Test')
                failed = False

        # Close the panel menu
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = oviewlib.close_panel_menu(self.driver, self.all_loggers, retrydict,
                                               self.sleepdict, pmn)

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testPanelMenuColors', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
