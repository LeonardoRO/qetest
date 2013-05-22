# loglib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import logging
import os
import time

def logfile(name, logpath, browser=None):
    if browser:
        logname = '%s.%s.%s.log' % (name, time.strftime('%Y_%m_%d'), browser)
    else:
        logname = '%s.%s.log' % (name, time.strftime('%Y_%m_%d'))
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    logfile = os.path.join(logpath, logname)

    return logfile

def test_logger(browser, suitename, logname, opts):
    """Create and format regular logging.

    Args
      name: string - name of the logging object.
      browser: string - name of web browser used in testing
      opts: dictionary - all of the command line arguments.

    Returns:
      logger: object - Formatted logging object
    """

    logger = logging.getLogger(logname)
    
    logger.setLevel(getattr(logging, opts.loglevel.upper()))
    ch = logging.StreamHandler()
    if opts.stdout == 'match':
        ch.setLevel(getattr(logging, opts.loglevel.upper()))
    else:
        ch.setLevel(getattr(logging, opts.stdout.upper()))

    fh = logging.FileHandler(logfile(suitename, opts.logpath, browser))
    ch_fmt = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s', datefmt='%H:%M:%S %Z')
    fh_fmt = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s',
                               datefmt='%a %Y-%m-%d %H:%M:%S %Z')
    fh.setFormatter(fh_fmt)
    logger.addHandler(fh)
    if not opts.silent:
        ch.setFormatter(ch_fmt)
        logger.addHandler(ch)

    return logger

def trace_logger(opts):
    tracelogger = logging.getLogger('tracelogger')
    tracelogger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile('stacktrace.errors', opts.logpath))
    fh_fmt = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s',
                               datefmt='%a %Y-%m-%d %H:%M:%S %Z')
    fh.setFormatter(fh_fmt)
    tracelogger.addHandler(fh)

    return tracelogger

def logDuration(start_time, test, logger):
    """How long a test took, format the output, send it to the log.

    Args
      start_time: float - Time test was started in milliseconds as
                  time.time() * 1000
      test: string - Name of the test being run.
      logger: object - Logging object for current test module.
    """

    current_time = round(time.time() * 1000)
    milliseconds = int(current_time) - int(start_time)
    total_seconds = (int(current_time) - int(start_time)) / 1000
    modulo_milli = (int(current_time) - int(start_time)) % 1000
    total_minutes = ((int(current_time) - int(start_time)) / 1000) / 60
    seconds = ((int(current_time) - int(start_time)) / 1000) % 60
    hours = total_minutes / 60
    minutes = total_minutes % 60
    runtime = None

    if minutes > 0 and minutes < 10:
        str_minutes = '0%s' % minutes
    elif minutes > 9:
        str_minutes = str(minutes)
    else:
        str_minutes = '00'

    if seconds > 0 and seconds < 10:
        str_seconds = '0%s' % seconds
    elif seconds > 9:
        str_seconds = str(seconds)
    else:
        str_seconds = '00'

    if hours > 0:
        runtime = ('%s:%s:%s' % (hours, str_minutes, str_seconds))
    elif minutes > 0:
        runtime = ('%s:%s' % (str_minutes, str_seconds))

    if runtime:
        logger.info('Total runtime for %s: %s (%s millisconds)' %
                    (test, runtime, milliseconds))
    elif total_seconds > 0 and total_seconds < 60:
        logger.info('Total runtime for %s: %s.%s seconds' %
                    (test, total_seconds, modulo_milli))
    else:
        logger.info('Total runtime for %s: %s milliseconds' % (test, milliseconds))

def logPassFail(test, totals, failed, starttime, logger, retrydict):
    """Log pass or fail results for individual modules.

    Args
      test: string - Name of test module.
      totals: dictionary - Total results from all modules.  Includes passed,
        failed, retries, executed, total and max_retries.
      failed: boolean - If true, module failed.
      starttime: float - Time testing began (rounded * 1000 time.time)
      logger: object - Logging object.
      retries: int - Retry count.
      max_retries: int - Maximum number of retries allowed.

    Returns updated totals dictionary
    """
    if retrydict['retries'] > 0:
        failed_text = '### FAILED ### - %s (Retry: %s)' % (test, retrydict['retries'])
        passed_text = '*** PASSED *** - %s (Retry: %s)' % (test, retrydict['retries'])
        end_text = 'End ==> %s (Retry: %s)' % (test, retrydict['retries'])
    else:
        failed_text = '### FAILED ### - %s' % test
        passed_text = '*** PASSED *** - %s' % test
        end_text = 'End ==> %s' % test

    if failed:
        if retrydict['retries'] >= retrydict['max_retries']:
            logger.error(failed_text)
            totals.update(failed = totals['failed'] + 1)
            totals['failed_testnames'] = [test]
        else:
            logger.info(failed_text)

    else:
        logger.info(passed_text)
        totals.update(passed = totals['passed'] + 1)

    logDuration(starttime, test, logger)
    logger.info(end_text)

    return totals

def logTotalTestResults(grand_totals, logger, gorked,):
    """Log final results for a test suite.

    Args
      grand_totals: dictionary - Total results from all modules.  Includes passed,
        failed, executed, total, and failed_testnames.
      logger: object - Logging object for current test module.
      gorked: boolean - True if test fails with unhandled exeption.
    """

    if gorked:
        logger.error('Unable to report total PASSED/FAILED because the script '
                     'exited before completion with an unknown exception')
    elif grand_totals['total'] > 0:
        total_modules = grand_totals['passed'] + grand_totals['failed']
        logger.info('PASSED/FAILED/TOTAL -- %s/%s/%s' %
                         (grand_totals['passed'], grand_totals['failed'], total_modules))
        percent_passed = float(grand_totals['passed']) / float(total_modules)
        percent_failed = float(grand_totals['failed']) / float(total_modules)
        if percent_passed == 1.0:
            logger.info('{0:.2%} Passed'.format(percent_passed))
        elif percent_failed == 1.0:
            logger.info('{0:.2%} Failed'.format(percent_failed))
        else:
            logger.info('{0:.2%} Passed'.format(percent_passed))
            logger.info('{0:.2%} Failed'.format(percent_failed))
        logger.info('Total individual tests executed: '
                        '%s of %s' % (grand_totals['executed'], grand_totals['total']))
        if grand_totals['failed_testnames']:
                logger.info('Failed Module(s): %s' % ', '.join(grand_totals['failed_testnames']))
    else:
        logger.error('Unable to report total PASSED/FAILED because one or more '
                  'tests exited without reporting their status.')

def logErrors(all_loggers, retrydict, trace=None, msg=None, error=None):
    logger = all_loggers[0]
    trace_logger = all_loggers[1]
    if retrydict['retries'] < retrydict['max_retries']:
        if msg:
            logger.debug(msg)
        if error:
            logger.debug(error)
    else:
        if msg:
            logger.error(msg)
        if error:
            logger.error(error)

    if trace:
        trace_logger.error('-' * 60)
        for line in trace.splitlines():
            trace_logger.error(line)
        trace_logger.error('-' * 60)
