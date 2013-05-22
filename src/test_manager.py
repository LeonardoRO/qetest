# test_manager.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import logging
import random
import string
import sys
import time

import qetest.src.libs.loglib as loglib
import qetest.src.libs.sellib as sellib

from qetest.src.tests.nova import ALL_TEST_KLASSES as novatests
from qetest.src.tests.lbaas import ALL_TEST_KLASSES as lbaastests
from qetest.src.tests.dns import ALL_TEST_KLASSES as dnstests
from qetest.src.tests.files import ALL_TEST_KLASSES as filestests

class TestManager(object):

    def __init__(self, conf):
        self.conf = conf
        self.starttime = round(time.time() * 1000)
        self.session_id = ''.join(random.sample(string.letters + string.digits, 32))
        self.trace_logger = loglib.trace_logger(self.conf.opts)
        self.test_klasses = []
        for service in self.conf.services:
            if service == 'nova' or service == 'all':
                self.test_klasses.extend(novatests)
            if service == 'lbaas' or service == 'all':
                self.test_klasses.extend(lbaastests)
            if service == 'dns' or service == 'all':
                self.test_klasses.extend(dnstests)
            if service == 'files' or service == 'all':
                self.test_klasses.extend(filestests)
            

    def setup(self, browser, suitename, logname):
        filelogger = loglib.test_logger(browser, suitename, logname, self.conf.opts)
        all_loggers = (filelogger, self.trace_logger)

        return all_loggers

    def start_driver(self, browser, logger):
        driver = sellib.select_driver(browser, logger)

        return driver

    def teardown(self, logger, driver):
        logger.info('-->> End ' + self.conf.suitename + ' suite <<--')
        driver.quit()
        loglib.logDuration(self.starttime, self.conf.suitename + ' suite', logger)

    def find_tests(self, all_loggers, driver):
        tests = []


        for klass in self.test_klasses:
            templist = []
            testinst = klass(all_loggers, self.conf, driver)
            for key in klass.__dict__.keys():
                if key[:4] == 'test':
                    templist.append(key)
            testlist = [element for element in templist if element not in self.conf.excluded]
            for testname in testlist:
                test = getattr(testinst, testname)
                tests.append(test)

        return tests

    def list_tests(self):
        testnames = []
        for klass in self.test_klasses:
            for name in klass.__dict__.keys():
                if name[:4] == 'test':
                    testnames.append(name)

        return testnames

    def login(self, all_loggers, driver, retries):
        failed = True
        retrydict = dict(retries=retries, max_retries=self.conf.retry + 1)
        with sellib.login_handler(all_loggers, retrydict):
            driver.get('%s/accounts/' % self.conf.testurl)
            sellib.element_wait(driver.find_element_by_name, 'username',
                                element_action='send_keys', action_arg=self.conf.username)
            sellib.sleeper(self.conf.sleepdict)
            sellib.element_wait(driver.find_element_by_name, 'password',
                                element_action='send_keys', action_arg=self.conf.password)
            sellib.sleeper(self.conf.sleepdict)
            sellib.element_wait(driver.find_element_by_class_name, 'submit', element_action='click')
            sellib.sleeper(self.conf.sleepdict)
            failed = False

        return failed

    def increment_grand_totals(self, grand_totals, totals):
        for k, v in totals.iteritems():
            if k == 'failed_testnames':
                for name in totals[k]:
                    grand_totals[k].append(name)
            else:
                grand_totals[k] = grand_totals.get(k) + totals.get(k)
        
        return grand_totals


    def run_modules(self, tests):
        grand_totals = dict(passed=0, failed=0, executed=0, total=0, failed_testnames=[])
        for module in self.conf.modules:
            for test in tests:
                if module in str(test):
                    for retry in range(self.conf.retry + 1):
                        failed = True
                        (failed, totals) = test(retry)
                        grand_totals = self.increment_grand_totals(grand_totals, totals)
                        if not failed:
                            break
        return grand_totals
            

    def run_all(self, tests):
        grand_totals = dict(passed=0, failed=0, executed=0, total=0, failed_testnames=[])
        for test in tests:
            for retry in range(self.conf.retry + 1):
                failed = True
                (failed, totals) = test(retry)
                grand_totals = self.increment_grand_totals(grand_totals, totals)
                if not failed:
                    break

        return grand_totals

    def run(self):
        if self.conf.modules:
            testnames = self.list_tests()
            testmodules = [module for module in testnames if module in self.conf.modules]
            if len(testmodules) != len(self.conf.modules):
                sys.stderr.write('\nThe provided module(s) cannot be found within the list of '
                                 'available test methods.  Please try the --list_tests option.\n')
                sys.exit(1)

        total_failed = 0
        self.trace_logger.info('+=+=+=+ Session ID: ' + self.session_id + ' +=+=+=+')
        for browser in self.conf.browsers:
            logname = ''.join(random.sample(string.letters + string.digits, 32))
            all_loggers = self.setup(browser, self.conf.suitename, logname)
            logger = all_loggers[0]
            logger.info('+=+=+=+ Session ID: ' + self.session_id + ' +=+=+=+')
            logger.info('++>> Start ' + self.conf.suitename + ' suite <<++')
            logger.debug('Test URL: %s' % self.conf.testurl)
            logger.debug('Username: %s' % self.conf.username)
            driver = self.start_driver(browser, logger)
            tests = self.find_tests(all_loggers, driver)

            for retry in range(self.conf.retry + 2):
                failed = self.login(all_loggers, driver, retry)
                if not failed:
                    break
                elif retry < self.conf.retry + 1:
                    pass
                else:
                    self.teardown(logger, driver)
                    logger.error('Attempted to login %s times' % str(retry + 1))
                    logger.error('Exiting test suite -- not much sense in continuing if you can\'t '
                                 'login, eh?')
                    sys.exit(1)

            if self.conf.modules:
                grand_totals = self.run_modules(tests)
            else:
                grand_totals = self.run_all(tests)
            
            self.teardown(logger, driver)
            loglib.logTotalTestResults(grand_totals, logger, gorked=False,)
            logger.info('-=' * 30 + '-')

            if grand_totals['failed'] > 0:
                self.trace_logger.info('-=' * 30 + '-')
                total_failed += 1
            else:
                self.trace_logger.info(' ')
                self.trace_logger.info('-=' * 30 + '-')
            logging.shutdown()
        return True if total_failed > 0 else False

