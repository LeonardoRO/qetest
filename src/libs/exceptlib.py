# exceptlib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ListOrderComparisonError(Error):
    """Exception raised for errors between the ordering of two lists.

    Args:
        list1 -- First list being used for comparison
        list2 -- Second list being used for comparison
    """

    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    def __str__(self):
        self.msg = 'The two lists are ordered differently -- %s -- %s' % (self.list1, self.list2)

        return self.msg

class TextNotFoundError(Error):

    def __str__(self):
        self.msg = 'The necessary text could not be found'

        return self.msg