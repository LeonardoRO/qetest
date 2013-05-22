# batchtest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import string

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib
import qetest.src.libs.oviewlib as oviewlib

from qetest.src.tests.basetest import BaseTest

BATCH_PANEL = '//div[@id="panel-menu-batch"]/descendant::'

class BatchTest(BaseTest):
    """This class tests the overview page's batch operations"""

    def __init__(self, all_loggers, conf, driver):
        super(BatchTest, self).__init__(all_loggers, conf)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        (starttime, retrydict) = super(BatchTest, self).setup(retries, testname)
        failed = oviewlib.setup(self.driver, self.all_loggers, retrydict, self.sleepdict)
        return starttime, retrydict, failed
    
    def all_nodes(self, retrydict, totals):
        failed = True
        totals.update(executed = totals['executed'] + 1)
        with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                  'Unable to find the batch action toggle',
                                  'FAILED - Batch Toggle Test'):
            sellib.element_wait(self.driver.find_element_by_id, 'batch_action_toggle', 'click')
            self.logger.debug('All nodes selected')
            self.logger.info('PASSED - Batch Toggle Test')
            sellib.sleeper(self.sleepdict)
            failed = False

        return failed, totals

    def batch_sprocket(self, retrydict, totals):
        totals.update(executed = totals['executed'] + 1)
        failed = True
        with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                    'Unable to find the batch panel sprocket',
                                    'FAILED - Batch Panel Sprocket Test '):
            path = '//span[@class="batch_control_panel_button"]'
            sellib.element_wait(self.driver.find_element_by_xpath, path, 'click')
            self.logger.debug('Batch Control Panel selected')
            self.logger.info('PASSED - Batch Panel Sprocket Test')
            sellib.sleeper(self.sleepdict)
            failed = False

        return failed, totals

    def testBatchTags(self, retries):
        """Tests batch changes to tags (labels) for all test set nodes.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 8,}
        (starttime, retrydict, failed) = self.setup('testBatchTags', retries,)

        # Select all the nodes
        if not failed:
            (failed, totals) = self.all_nodes(retrydict, totals)

        # Click on the batch panel sprocket to bring up the 'tag' or 'color' option
        if not failed:
            (failed, totals) = self.batch_sprocket(retrydict, totals)

        # Click on the 'tag' option to bring up the tag panel
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to find the tag panel menu',
                                        'FAILED - Tag Panel Menu Test'):
                tagpath = ('%sdiv[attribute::class="panel-menuitem tag-panel-menuitem"]'
                           % BATCH_PANEL)
                sellib.element_wait(self.driver.find_element_by_xpath, tagpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the tag panel menu')
                self.logger.info('PASSED - Tag Panel Menu Test')
                failed = False

        # Create a new tag (session specific) and assign to all nodes
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            rand1 = ''.join(random.sample(string.letters + string.digits, 5))
            newtag = '%s-%s' % (random.choice(self.conf.peeps), rand1)
            newtagpath = ('%sdiv[contains(text(), "Search for or create a tag")]/'
                          'following-sibling::input' % BATCH_PANEL)
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to create tag "%s" for all nodes' % newtag,
                                        'FAILED - Custom Tag Creation Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, newtagpath, 'send_keys',
                                    newtag)
                sellib.sleeper(self.sleepdict)
                createpath = ('%sdiv[attribute::class="ck_widgets_action_button" and '
                             'contains(text(), "(create new)")]' % BATCH_PANEL)
                sellib.element_wait(self.driver.find_element_by_xpath, createpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Created tag "%s" for all the nodes' % newtag)
                self.logger.info('PASSED - Custom Tag Creation Test')
                failed = False

        # Remove the custom tag from all nodes
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to remove tag "%s" from the nodes'
                                        % newtag,
                                        'FAILED - Custom Tag Removal Test'):
                custtagpath = ('%sdiv[attribute::class="goog-inline-block ck_widgets_closable'
                               '_label" and contains(text(), "%s")]' % (BATCH_PANEL, newtag))
                sellib.element_wait(self.driver.find_element_by_xpath, custtagpath, 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Removed tag "%s" from all nodes' % newtag)
                self.logger.info('PASSED - Custom Tag Removal Test')
                failed = False

        # Re-add then re-remove the custom tag for all nodes.  Use the tag above
        # the text box to remove the tag as a test to confirm that it was added
        # back.

        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Failed to re-add/remove tag "%s"' % newtag,
                                        'FAILED - RE Add/Remove Tag Test'):
                addpath = ('%sdiv[attribute::class="ck_widgets_action_menuitem-content"'
                           ' and contains(text(), "%s")]' % (BATCH_PANEL, newtag))
                sellib.element_wait(self.driver.find_element_by_xpath, addpath, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '%sdiv[attribute::role="button" and contains(text(), "%s")]'
                                    % (BATCH_PANEL, newtag),
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Re-added then re-removed tag "%s" to all nodes' % newtag)
                self.logger.info('PASSED - RE Add/Remove Tag Test')
                failed = False

        # Completely delete the custom tag
        # TODO (dborin): Figure out how to verify that the custom tag was removed

        # NOTE: This uses the addpath value from the previous section
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to delete custom tag "%s"' % newtag,
                                        'FAILED - Custom Tag Deletion Test'):
                delpath = ('%s/following-sibling::div[attribute::class="ck_widgets_'
                           'action_button"]' % addpath)
                sellib.element_wait(self.driver.find_element_by_xpath, delpath, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//button[attribute::name="ok"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Custom tag "%s" deleted' % newtag)
                self.logger.info('PASSED - Custom Tag Deletion Test')
                failed = False

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testBatchTags', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testBatchColors(self, retries):
        """Tests batch color changes for all test set nodes.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """


        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 7,}
        (starttime, retrydict, failed) = self.setup('testBatchColors', retries,)

        colors = oviewlib.panel_colors()
        total_colors = len(colors)

        # Select all the nodes
        if not failed:
            (failed, totals) = self.all_nodes(retrydict, totals)

        # Click on the batch panel sprocket to bring up the 'tag' or 'color' option
        if not failed:
            (failed, totals) = self.batch_sprocket(retrydict, totals)
            

        # Click on the 'color' option to bring up the color panel
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the color panel menu',
                                        'FAILED - Batch Color Menu Test'):
                color_opt_path = ('%sdiv[attribute::class="panel-menuitem color-panel-menuitem"]'
                                  % BATCH_PANEL)
                sellib.element_wait(self.driver.find_element_by_xpath, color_opt_path, 'click')
                self.logger.info('Found color panel menu')
                self.logger.info('PASSED - Batch Color Menu Test')
                sellib.sleeper(self.sleepdict)
                failed = False

        # Cycle through some random colors
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            rand1 = random.randint(0, total_colors - 2)
            rand2 = rand1
            while rand2 == rand1:
                rand2 = random.randint(0, total_colors - 2)
            random_colors = (colors[rand1], colors[rand2], colors[total_colors - 1])
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to cycle through some random colors',
                                        'FAILED - Batch Color Change Test'):
                for kolor in random_colors:
                    colorpath = '//div[attribute::title="RGB %s"]' % kolor
                    sellib.element_wait(self.driver.find_element_by_xpath, colorpath, 'click')
                    sellib.sleeper(self.sleepdict)
                self.logger.debug('Random color selection succeeded')
                self.logger.info('PASSED - Batch Color Change Test')
                failed = False

        # Test the 'custom colors' input text box and close the batch panel menu
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to set a custom color',
                                        'FAILED - Batch Custom Color Test'):
                custompath = ('%sinput[attribute::class="label-input-label"]' % BATCH_PANEL)
                oviewlib.custom_colors(self.driver, self.logger, custompath, self.sleepdict)
                sellib.sleeper(self.sleepdict)
                self.logger.info('PASSED - Batch Custom Color Test')
                failed = False

        # Close the panel menu
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = oviewlib.close_panel_menu(self.driver, self.all_loggers, retrydict,
                                               self.sleepdict, BATCH_PANEL)

        totals.update(executed = totals['executed'] + 1)
        totals = loglib.logPassFail('testBatchColors', totals, failed, starttime, self.logger,
                                    retrydict)
        return failed, totals
