# config_manager.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import os
import selenium.webdriver.common.keys as keys
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # pylint: disable=C0103
sys.path.append(os.path.abspath(CURRENT_DIR + "/../../../")) # pylint: enable=C0103

import qetest.src.libs.optlib as optlib

class ConfigurationManager(object):

    def __init__(self, suitename):
        self.suitename = suitename
        (self.opts, self.args) = optlib.optionParser() # pylint: disable=W0612
        self.keys = keys.Keys() # pylint: enable=W0612
        self.dataset = self.opts.dataset
        self.sleepdict = {'sleep': self.opts.sleep, 'fast': self.opts.fast}
        self.peeps = ['Bjorn', 'Brad', 'Brian', 'Chris', 'Ed', 'Jigar', 'John', 'King', 'Lucy',
                      'Mark', 'Nachos', 'Shawn',]

        self.port = self.opts.port if self.opts.port else '8001'
        self.testurl = '%s:%s' % (self.opts.host, self.port)
        self.modules = self.opts.modules
        self.retry = self.opts.retry

        if self.opts.username:
            if not self.opts.password:
                sys.stderr.write('\nNo password supplied for user %s\n' % self.opts.username)
                sys.exit(1)
            else:
                self.username = self.opts.username
        else:
            self.username = self.opts.dataset

        if self.opts.password:
            if not self.opts.username:
                sys.stderr.write('\nPassword provided, but no username supplied\n')
                sys.exit(1)
            else:
                self.password = self.opts.password
        else:
            self.password = self.opts.dataset

        if not self.opts.logpath:
            self.opts.logpath = os.path.join(os.path.abspath(CURRENT_DIR + '/../'), 'logs')

        if self.opts.browsers:
            self.browsers = self.opts.browsers
        else:
            self.browsers = ['firefox']

        if self.opts.excluded:
            self.excluded = self.opts.excluded
        else:
            self.excluded = []

        if self.opts.services:
            if 'all' in self.opts.services:
                self.services = ['all']
            else:
                self.services = self.opts.services
        else:
            self.services = ['nova']
