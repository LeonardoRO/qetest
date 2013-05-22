# sellib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import math
import selenium.common.exceptions as selexcept
import sys
import time
import traceback

import qetest.src.libs.loglib as loglib
import qetest.src.libs.exceptlib as exceptlib

from contextlib import contextmanager
from selenium import webdriver

def select_driver(browser, logger):
    if browser == 'firefox':
        try:
            driver = webdriver.Firefox()
            log_useragent(driver, logger)
        except Exception, e:
            logger.exception(e)
            sys.exit(1)
    elif browser == 'chrome':
        try:
            driver = webdriver.Chrome()
            log_useragent(driver, logger)
        except Exception, e:
            logger.exception(e)
            sys.exit(1)

    return driver

def log_useragent(driver, logger):
    uagent = driver.execute_script('return (function () { return window.navigator.userAgent; }'
                                   ')();')
    logger.debug(uagent)

def element_wait(driver_func, func_value=None, element_action=None,
                 action_arg=None, duration=10.0, interval=0.25):
    caught_error = None
    for i in range(0, int(math.ceil(duration/interval))):
        try:
            myelement = driver_func(func_value) if func_value else driver_func
            if element_action:
                myaction = getattr(myelement, element_action)
                if action_arg:
                    myaction(action_arg)
                else:
                    myaction()
                caught_error = None
            else:
                caught_error = None
                return myelement
        except (selexcept.NoSuchElementException, selexcept.ElementNotVisibleException,
                selexcept.StaleElementReferenceException) as e:
            caught_error = e
            time.sleep(interval)
        if not caught_error:
            break
    if caught_error:
        raise caught_error


def elements_wait(driver, driver_value, element_id='xpath', duration=10.0, interval=0.25):
    caught_error = None
    for i in range(0, int(math.ceil(duration/interval))):
        try:
            driver.find_element(by=element_id, value=driver_value)
            myelements = driver.find_elements(by=element_id, value=driver_value)
            caught_error = None
            return myelements
        except (selexcept.NoSuchElementException, selexcept.ElementNotVisibleException,
                selexcept.StaleElementReferenceException) as e:
            caught_error = e
            time.sleep(interval)
        if not caught_error: break
    if caught_error: raise caught_error
    

@contextmanager
def error_handler(driver, all_loggers, retrydict, msg, testcase=None):
    """This decorator uses the contextlib.contextmanager to handle the majority
       of the try/except statements used in the test suite.
    """
    totals = dict(passed=0, failed=0, executed=0, total=0)
    logger = all_loggers[0]
    try:
        yield
    except (selexcept.NoSuchElementException, selexcept.ElementNotVisibleException,
            selexcept.StaleElementReferenceException, selexcept.WebDriverException,
            exceptlib.ListOrderComparisonError, exceptlib.TextNotFoundError, IndexError), error:
        loglib.logErrors(all_loggers, retrydict, traceback.format_exc(), msg, error)
        if testcase: logger.info(testcase)
    except Exception, error:
        driver.quit()
        loglib.logTotalTestResults(totals, logger, gorked=True)
        loglib.logErrors(all_loggers, retrydict, traceback.format_exc(), msg, error)
        logger.info('-=' * 30 + '-')
        sys.exit(1)

@contextmanager
def login_handler(all_loggers, retrydict):
    """This decorator uses the contextlib.contextmanager to handle login failures."""

    try:
        yield
    except Exception, error:
        msg = 'Unable to initiate testing -- cannot log into Reach UI'
        loglib.logErrors(all_loggers, retrydict, traceback.format_exc(), msg, error)

def sleeper(sleepdict):
    """Determines sleep interval between steps in tests.

    Args:
      sleepdict: dictionary - sleep value (float) and fast (bool)
    """

    if not sleepdict['fast']:
        time.sleep(sleepdict['sleep'])
