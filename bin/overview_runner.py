#!/usr/bin/env python

# overview_runner.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # pylint: disable=C0103
sys.path.append(os.path.abspath(CURRENT_DIR + "/../../")) # pylint: enable=C0103

from qetest.src.config_manager import ConfigurationManager
from qetest.src.test_manager import TestManager

if __name__ == '__main__':

    failed = False
    conf = ConfigurationManager('Overview')
    testmgr = TestManager(conf)
    if testmgr.conf.opts.list_tests:
        testlist = testmgr.list_tests()
        sys.stdout.write('\nAvailable test methods:\n\n')
        for test in testlist:
            sys.stdout.write(test + '\n')
    else:
        failed = testmgr.run()

    sys.exit(1) if failed else sys.exit(0)
