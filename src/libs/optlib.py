# optlib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

from optparse import OptionParser

def optionParser():
    parser = OptionParser()
    parser.add_option('--browser',
                      dest='browsers',
                      choices=['firefox', 'chrome'],
                      action='append',
                      help='Browser(s) to run tests in. Options are firefox or chrome. [default: firefox]')
    parser.add_option('--host',
                      dest='host',
                      default='http://127.0.0.1',
                      help='''Host nickname from hostconf.py or FQDN/IP to test
                      against [default: %default]''')
    parser.add_option('--port',
                      dest='port',
                      help='HTTP port')
    parser.add_option('--dataset',
                      dest='dataset',
                      default='qetest_alpha',
                      help='Test dataset [default: %default]')
    parser.add_option('--username',
                      dest='username',
                      help='Overrides dataset username')
    parser.add_option('--password',
                      dest='password',
                      help='Overrides dataset password')
    parser.add_option('--loglevel',
                      dest='loglevel',
                      default='debug',
                      choices=['info', 'debug', 'warn', 'error', 'critical'],
                      help='Logging level for logfile [default: %default]')
    parser.add_option('--stdout',
                      dest='stdout',
                      default='info',
                      choices=['info', 'debug', 'warn', 'error', 'critical',
                               'match'],
                      help='''Logging level for screen output ('match' matches
                           logfile level) [default: %default]''')
    parser.add_option('--logpath',
                      dest='logpath',
                      default='',
                      help='''Directory location (path) for log file(s).  This
                      will create the directory if it doesn't already exist.  
                      [default: qetest/logs]''')
    parser.add_option('--silent',
                      dest='silent',
                      action='store_true',
                      help='Turn off logging to STDOUT')
    parser.add_option('--fast',
                      dest='fast',
                      action='store_true',
                      help='Makes testing run fast by turning off all sleeps.')
    parser.add_option('--sleep',
                      dest='sleep',
                      default=2.0,
                      type='float',
                      help='Universal time.sleep() value. [default: %default]')
    parser.add_option('--retry',
                      dest='retry',
                      default=2,
                      type='int',
                      help='''Number of times to retry failed tests.
                      [default: %default]''')
    parser.add_option('--module',
                      dest='modules',
                      action='append',
                      help='Names of individual test modules to be run')
    parser.add_option('--service',
                      dest='services',
                      action='append',
                      choices=['nova', 'lbaas', 'dns', 'files', 'all'],
                      help='Service(s) to be tested (i.e. nova or lbaas)')
    parser.add_option('--exclude',
                      dest='excluded',
                      action='append',
                      help='Names of individual test modules to exclude')
    parser.add_option('--node',
                      dest='nodes',
                      action='append',
                      help='Names of individual test nodes to use (overrides nodeconf.py)')
    parser.add_option('--list_tests',
                      dest='list_tests',
                      action='store_true',
                      help='Show a list of available test methods (modules)')
    (opts, args) = parser.parse_args()

    return opts, args
