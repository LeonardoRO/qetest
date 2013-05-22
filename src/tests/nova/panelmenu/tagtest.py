# powertest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import string

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest

class PanelTagTest(PanelBaseTest):
    """This class tests the panel menu tag option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelTagTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelTagTest, self).setup(retries, testname)

    def testPanelMenuTags(self, retries):
        """Tests for changing individual node's tag panel tags (labels).

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 6,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testPanelMenuTags', retries)

        # Click on the 'tag' option to bring up the tag panel
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            tagpanelpath = ('%sspan[attribute::class="panel-menuitem-icon'
                            ' tag-panel-menuitem-icon"]' % pmn)
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to find the tag panel menu',
                                        'FAILED - Tag Panel Menu Test'):
                self.driver.find_element_by_xpath(tagpanelpath).click()
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on "tag" menu item')
                self.logger.info('PASSED - Tag Panel Menu Test')
                failed = False

        # Create a new tag (session specific) and assign it
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            rand1 = ''.join(random.sample(string.letters + string.digits, 5))
            newtag = '%s-%s' % (random.choice(self.conf.peeps), rand1)
            newtagpath = ('%sdiv[contains(text(), "Search for or create a tag")]/'
                          'following-sibling::input' % pmn)
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to create tag "%s"' % newtag,
                                        'FAILED - Custom Tag Creation Test'):
                inputtag = sellib.element_wait(self.driver.find_element_by_xpath, newtagpath)
                inputtag.send_keys(newtag)
                createpath = ('%sdiv[attribute::class="ck_widgets_action_button" and '
                             'contains(text(), "(create new)")]' % pmn)
                sellib.element_wait(self.driver.find_element_by_xpath, createpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Created tag "%s"' % newtag)
                self.logger.info('PASSED - Custom Tag Creation Test')
                failed = False

        # Remove the custom tag
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            removalpath = ('%sdiv[attribute::class="goog-inline-block ck_widgets_closable'
                      '_label" and contains(text(), "%s")]' % (pmn, newtag))
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to remove tag "%s"' % newtag,
                                        'FAILED - Custom Tag Removal Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, removalpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Removed tag "%s"' % newtag)
                self.logger.info('PASSED - Custom Tag Removal Test')
                failed = False

        # Re-add then re-remove the custom tag.  Use the tag above the
        # text box to remove the tag as a test to confirm that it was added back.

        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            widgetpath = ('%sdiv[@class="ck_widgets_action_menuitem-content"' ' and contains(text(), "%s")]'
                       % (pmn, newtag))
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to re-add/remove tag "%s"' % newtag,
                                        'FAILED - RE Add/Remove Tag Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, widgetpath, 'click')
                sellib.sleeper(self.sleepdict)
                newtag_path = '%sdiv[@role="button" and ' 'contains(text(), "%s")]' % (pmn, newtag)
                sellib.element_wait(self.driver.find_element_by_xpath, newtag_path, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Re-added then re-removed tag "%s"' % newtag)
                self.logger.info('PASSED - RE Add/Remove Tag Test')
                failed = False

        # Completely delete the custom tag.
        # TODO (dborin): Figure out how to verify that the custom tag was removed

        # NOTE: This uses the widgetpath value from the previous section
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            deletepath = ('%s/following-sibling::div[attribute::class="ck_widgets_'
                       'action_button"]' % widgetpath)
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to delete custom tag "%s"' % newtag,
                                        'FAILED - Custom Tag Deletion Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, deletepath, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[@name="ok"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Custom tag "%s" deleted' % newtag)
                self.logger.info('PASSED - Custom Tag Deletion Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testPanelMenuTags', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals
