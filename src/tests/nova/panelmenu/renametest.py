# renametest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import string

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest


class PanelRenameTest(PanelBaseTest):
    """This class tests the panel menu node renaming option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelRenameTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelRenameTest, self).setup(retries, testname)

    def testRenaming(self, retries):
        """Test node renaming functionality.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 4,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testRenaming', retries)

        # Click on the panel menu's rename option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the rename menu item',
                                        'FAILED - Rename Menu Item Test'):
                self.driver.find_element_by_xpath('%sdiv[attribute::class="panel-menuitem'
                                             ' rename-panel-menuitem"]' % pmn).click()
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Located rename option in the panel menu')
                self.logger.info('PASSED - Rename Menu Item Test')
                failed = False

        # Verify existing node name and change the name of the node to something
        # session specific
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to rename node %s' % testnode,
                                        'FAILED - Rename Node Test Pt. 1'):
                rand1 = ''.join(random.sample(string.letters + string.digits, 5))
                newnodename = '%s-%s' % (random.choice(self.conf.peeps), rand1)
                current_name = ('%sdiv[attribute::class="input-panel"]/'
                                'descendant::input[attribute::class="input-panel-input'
                                ' label-input"]' % pmn)
                name_change = sellib.element_wait(self.driver.find_element_by_xpath, current_name)
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(name_change, element_action='clear')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(name_change, element_action='send_keys',
                                    action_arg=newnodename)
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(name_change, element_action='send_keys',
                                    action_arg=self.keys.RETURN)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Successfully renamed node %s to %s' % (testnode, newnodename))
                self.logger.info('PASSED - Rename Node Test Pt. 1')
                failed = False

        # Verify the new node name and change the node name back to it's
        # starting name
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to change node name back to %s'
                                        % testnode,
                                        'FAILED - Rename Node Test Pt. 2'):
                current_name = ('%sdiv[attribute::class="input-panel"]/'
                                'descendant::input[attribute::class="input-panel-input'
                                ' label-input"]' % pmn)
                change_back = sellib.element_wait(self.driver.find_element_by_xpath, current_name)
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(change_back, element_action='clear')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(change_back, element_action='send_keys',
                                    action_arg=testnode)
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(change_back, element_action='send_keys',
                                    action_arg=self.keys.RETURN)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Successfully renamed node %s back to %s' % (newnodename,
                                                                          testnode))
                self.logger.info('PASSED - Rename Node Test Pt. 2')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testRenaming', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals
