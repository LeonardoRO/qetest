# resizetest.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import re

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova.panelmenu.panelbasetest import PanelBaseTest
from qetest.src.libs.exceptlib import ListOrderComparisonError


class PanelResizeTest(PanelBaseTest):
    """This class tests the panel menu power option."""

    def __init__(self, all_loggers, conf, driver):
        super(PanelResizeTest, self).__init__(all_loggers, conf, driver)
        self.driver = driver
    
    @classmethod
    def all_methods(klass):
        return [name for name in klass.__dict__.keys() if 'test' == name[:4]]

    def setup(self, testname, retries):
        return super(PanelResizeTest, self).setup(retries, testname)

    def click_resize_option(self, pmn, testnode):
        """Find and click on the resize option in the panel menu.

        Args:
            pmn -- string - panel menu node number
            testnode -- string - randomly selected node name
        """

        resizepath = ('%sdiv[@class="panel-menuitem resize-panel-menuitem"]' % pmn)
        sellib.element_wait(self.driver.find_element_by_xpath, resizepath, 'click')
        sellib.sleeper(self.sleepdict)
        self.logger.debug('Located resize option for node %s' % testnode)

    def get_flavors(self, section_number):
        """Find all the flavor elements for a particular column in the resize flavor table.

        Args:
            section_number -- int - completes the XPath for the various columns in the table.

        Returns:
            List of elements for a specific column (i.e. RAM or Disk)
        """
        
        flavorpath = ('//div[@class="ck-widgets-split-menuitem-section ck-widgets-split-'
                      'menuitem-section-%s"]' % section_number)

        return sellib.elements_wait(self.driver, flavorpath)

    def sortable_int(self, value):
        return int(re.sub(r'\$?([0-9]*).*', '\\1', str(value)))

    def compare_sorting(self, list1, list2):
        if len(list1) != len(list2):
            raise ListOrderComparisonError(list1, list2)

        for x in range(len(list1)):
            if list1[x] != list2[x]:
                raise ListOrderComparisonError(list1, list2)

    def testResize(self, retries):
        """Test the basic panel menu resize functionality.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 4,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testResize', retries)
        totals.update(executed = totals['executed'] + 1)

        # Click on the resize option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the resize option',
                                        'FAILED - Resize Option Test'):
                self.click_resize_option(pmn, testnode)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the resize option')
                self.logger.info('PASSED - Resize Option Test')
                failed = False

        # Select the first flavor in the flavor table list        
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or click on the first flavor in the table',
                                        'FAILED - Resize Flavor Selection Test'):
                
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[@class="radio-menuitem-checkbox"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on the first choice in the flavor table')
                self.logger.info('PASSED - Resize Flavor Selection Test')
                failed = False

        # Click the resize server button and then OK the change
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or click on the first flavor in the table',
                                        'FAILED - Resize Node Test'):
                resize_button_path = ('//button[@class="resize-button goog-button" '
                                      'and contains(text(), "Resize Server")]')
                sellib.element_wait(self.driver.find_element_by_xpath, resize_button_path, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath, '//button[@name="ok"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Successfully able to resize node')
                self.logger.info('PASSED - Resize Node Test')
                failed = False

        totals = loglib.logPassFail('testResize', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testCancelResize(self, retries):
        """Test the basic panel menu 'resize' then 'cancel' option.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testResizeCancel', retries)
        totals.update(executed = totals['executed'] + 1)
        resize_button_path = ('//button[@class="resize-button goog-button" and '
                              'contains(text(), "Resize Server")]')

        # Click on the resize option
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find the resize option',
                                        'FAILED - Resize Option Test'):
                self.click_resize_option(pmn, testnode)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Found the resize option')
                self.logger.info('PASSED - Resize Option Test')
                failed = False

        # Select the first flavor in the flavor table list        
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or click on the first flavor in the table',
                                        'FAILED - Resize Flavor Selection Test'):
                
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[@class="radio-menuitem-checkbox"]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on the first choice in the flavor table')
                self.logger.info('PASSED - Resize Flavor Selection Test')
                failed = False

        # Click the resize server button and then cancel the change
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or click on the first flavor in the table',
                                        'FAILED - Resize Node Test'):
                
                sellib.element_wait(self.driver.find_element_by_xpath, resize_button_path, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath, '//button[@name="cancel"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on cancel link')
                self.logger.info('PASSED - Resize Cancel Test')
                failed = False

        # Click the resize server button and then OK the change
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or click on the first flavor in the table',
                                        'FAILED - Resize Node Test'):
                sellib.element_wait(self.driver.find_element_by_xpath, resize_button_path, 'click')
                sellib.sleeper(self.sleepdict)
                sellib.element_wait(self.driver.find_element_by_xpath, '//button[@name="ok"]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on ok button')
                self.logger.info('PASSED - Resize OK Test')
                failed = False

        totals = loglib.logPassFail('testResizeCancel', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testRAMSorting(self, retries):
        """Test the sorting for RAM in the resize flavor table.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testRAMSorting', retries)
        totals.update(executed = totals['executed'] + 1)

        # Get the flavors of RAM
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or gather the resize RAM flavors',
                                        'FAILED - RAM Flavor Data Test'):
                self.click_resize_option(pmn, testnode)
                flavoritems0 = self.get_flavors(0)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('RAM flavor data located and gathered for node %s' % testnode)
                self.logger.info('PASSED - RAM Flavor Data Test')
                failed = False

        # Test RAM default list sorting
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Default RAM column sorted incorrectly',
                                        'FAILED - Resize: Default RAM Sort Test'):
                def_ram_list = []
                for def_ram_element in flavoritems0:
                    def_ram_list.append(int(self.sortable_int(def_ram_element.text)))
                sorted_ram_list = sorted(def_ram_list)
                self.compare_sorting(def_ram_list, sorted_ram_list)
                self.logger.debug('Default RAM column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Default RAM Sort Test')
                failed = False

        # Test sorting after reversing the list
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reversed RAM column sorted incorrectly',
                                        'FAILED - Resize: Reversed RAM Sort Test'):
                rev_sorted_ram_list = sorted(sorted_ram_list, reverse=True)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "RAM")]', 'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on RAM column header to put flavor table in reverse '
                                  'RAM sort order')

                rev_flavoritems0 = self.get_flavors(0)
                rev_ram_list = []
                for rev_element in rev_flavoritems0:
                    rev_ram_list.append(int(self.sortable_int(rev_element.text)))
                self.compare_sorting(rev_ram_list, rev_sorted_ram_list)
                self.logger.debug('Reversed RAM column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reversed RAM Sort Test')
                failed = False

        # Test sorting after reseting the list back to default 
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reset RAM column sorted incorrectly',
                                        'FAILED - Resize: Reset RAM Sort Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "RAM")]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on RAM column header to put flavor table back to '
                                  'default RAM sort order')
                ret_flavoritems0 = self.get_flavors(0)
                ret_ram_list = []
                for ret_element in ret_flavoritems0:
                    ret_ram_list.append(int(self.sortable_int(ret_element.text)))
                self.compare_sorting(ret_ram_list, def_ram_list)
                self.logger.debug('Reset RAM column sorting correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reset RAM Sort Test')
                failed = False

        totals = loglib.logPassFail('testRAMSorting', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testDiskSorting(self, retries):
        """Test the sorting for Disk in the resize flavor table.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testDiskSorting', retries)
        totals.update(executed = totals['executed'] + 1)

        # Get the flavors of Disk
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or gather the resize Disk flavors',
                                        'FAILED - Disk Flavor Data Test'):
                self.click_resize_option(pmn, testnode)
                flavoritems1 = self.get_flavors(1)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Disk flavor data located and gathered for node %s' % testnode)
                self.logger.info('PASSED - Disk Flavor Data Test')
                failed = False

        # Test Disk default list sorting
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Default Disk column sorted incorrectly',
                                        'FAILED - Resize: Default Disk Sort Test'):
                def_disk_list = []
                for def_disk_element in flavoritems1:
                    def_disk_list.append(int(self.sortable_int(def_disk_element.text)))
                sorted_disk_list = sorted(def_disk_list)
                self.compare_sorting(def_disk_list, sorted_disk_list)
                self.logger.debug('Default Disk column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Default Disk Sort Test')
                failed = False

        # Test sorting after reversing the list
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reversed Disk column sorted incorrectly',
                                        'FAILED - Resize: Reversed Disk Sort Test'):
                rev_sorted_disk_list = sorted(sorted_disk_list, reverse=True)
                # Click once to select the header, then a second time to reverse it
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Disk")]',
                                    'click')
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Disk")]',
                                    'click')
                self.logger.debug('Clicked on Disk column header to put flavor table in reverse '
                                  'Disk sort order')
                rev_flavoritems1 = self.get_flavors(1)
                sellib.sleeper(self.sleepdict)

                rev_disk_list = []
                for rev_element in rev_flavoritems1:
                    rev_disk_list.append(int(self.sortable_int(rev_element.text)))
                self.compare_sorting(rev_disk_list, rev_sorted_disk_list)
                self.logger.debug('Reversed Disk column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reversed Disk Sort Test')
                failed = False

        # Test sorting after reseting the list back to default 
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reset Disk column sorted incorrectly',
                                        'FAILED - Resize: Reset Disk Sort Test'):

                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Disk")]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on Disk column header to put flavor table back to '
                                  'default Disk sort order')
                ret_flavoritems1 = self.get_flavors(1)
                ret_disk_list = []
                for ret_element in ret_flavoritems1:
                    ret_disk_list.append(int(self.sortable_int(ret_element.text)))
                
                self.compare_sorting(ret_disk_list, def_disk_list)
                self.logger.debug('Reset Disk column sorting correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reset Disk Sort Test')
                failed = False

        totals = loglib.logPassFail('testDiskSorting', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals

    def testPriceSorting(self, retries):
        """Test the sorting for Price in the resize flavor table.

        Args:
          retries: int - number of times a test has been run

        Returns:
          failed: boolean - If true, one test within the module has failed
        """

        totals = {'passed': 0, 'failed': 0, 'executed': 0, 'total': 5,}
        (starttime, retrydict, failed, pmn, testnode) = self.setup('testPriceSorting', retries)
        totals.update(executed = totals['executed'] + 1)

        # Get the flavors of Price
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Unable to find or gather the resize Price flavors',
                                        'FAILED - Price Flavor Data Test'):
                self.click_resize_option(pmn, testnode)
                flavoritems2 = self.get_flavors(2)
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Price flavor data located and gathered for node %s' % testnode)
                self.logger.info('PASSED - Price Flavor Data Test')
                failed = False

        # Test Price list sorting
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Price column sorted correctly',
                                        'FAILED - Resize: Default Price Sort Test'):
                def_price_list = []
                for def_price_element in flavoritems2:
                    def_price_list.append(int(self.sortable_int(def_price_element.text)))
                sorted_price_list = sorted(def_price_list)
                self.compare_sorting(def_price_list, sorted_price_list)
                self.logger.debug('Default Price column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Default Price Sort Test')
                failed = False

        # Test sorting after reversing the list
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reversed Price column sorted incorrectly',
                                        'FAILED - Resize: Reversed Price Sort Test'):
                rev_sorted_price_list = sorted(sorted_price_list, reverse=True)
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Price")]',
                                    'click')
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Price")]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                rev_flavoritems2 = self.driver.find_elements_by_xpath('//div[@class="ck-widgets-split-'
                                                                   'menuitem-section ck-widgets-split-'
                                                                   'menuitem-section-2"]')
                self.logger.debug('Clicked on Price column header to put flavor table in reverse '
                                  'Price sort order')
                
                rev_price_list = []
                for rev_element in rev_flavoritems2:
                    rev_price_list.append(int(self.sortable_int(rev_element.text)))
                self.compare_sorting(rev_price_list, rev_sorted_price_list)
                self.logger.debug('Reversed Price column sorted correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reversed Price Sort Test')
                failed = False

        # Test sorting after reseting the list back to default 
        if not failed:
            totals.update(executed = totals['executed'] + 1)
            failed = True
            with sellib.error_handler(self.driver, self.all_loggers, retrydict,
                                        'Reset Price column sorted incorrectly',
                                        'FAILED - Resize: Reset Price Sort Test'):
                sellib.element_wait(self.driver.find_element_by_xpath,
                                    '//div[contains(text(), "Price")]',
                                    'click')
                sellib.sleeper(self.sleepdict)
                self.logger.debug('Clicked on Price column header to put flavor table back to '
                                  'default Price sort order')
                ret_flavoritems2 = self.driver.find_elements_by_xpath('//div[@class="ck-widgets-split-'
                                                                   'menuitem-section ck-widgets-split-'
                                                                   'menuitem-section-2"]')
                ret_price_list = []
                for ret_element in ret_flavoritems2:
                    ret_price_list.append(int(self.sortable_int(ret_element.text)))
                self.compare_sorting(ret_price_list, def_price_list)
                self.logger.debug('Price column sorting correctly for node %s' % testnode)
                self.logger.info('PASSED - Resize: Reset Price Sort Test')
                failed = False

        totals = loglib.logPassFail('testPriceSorting', totals, failed, starttime, self.logger,
                                    retrydict)

        return failed, totals
