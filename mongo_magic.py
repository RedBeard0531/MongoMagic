"""
This module is designed to make it easier to write queries for MongoDB in python

Author: Mathias Stearn <redbeard0531@gmail.com>
Date: April 5, 2010
License: Do what you want, just don't blame me if your computer catches fire.
"""

__all__ = ["M", "AND"]

class Magic(dict):
    def __init__(self, field=""):
        self.__field = field

    def __getattribute__(self, name):
        if name.startswith('_Magic__') or name.isupper():
            return object.__getattribute__(self, name)
        else:
            return Magic(self.__field + '.' + name)

    def __get_dict(self):
        if self.__field not in self:
            self[self.__field] = {}
        return self[self.__field]

    def __lt__(self, rhs): self.__get_dict()['$lt'] = rhs; return self
    def __gt__(self, rhs): self.__get_dict()['$gt'] = rhs; return self
    def __le__(self, rhs): self.__get_dict()['$lte'] = rhs; return self
    def __ge__(self, rhs): self.__get_dict()['$gte'] = rhs; return self
    def __ne__(self, rhs): self.__get_dict()['$ne'] = rhs; return self
    def __eq__(self, rhs): self[self.__field] = rhs; return self

    def __array_helper(self, name, args):
        if len(args) == 1:
            args = list(args[0])
        self.__get_dict()[name] = args
        return self

    def IN(self, *args): return self.__array_helper('$in', args)
    def NIN(self, *args): return self.__array_helper('$nin', args)
    def ALL(self, *args): return self.__array_helper('$all', args)

    def EXISTS(self, does_it=True):
        self.__get_dict()['$exists'] = does_it
        return self

    def RE(self, regex, opts=''):
        self.__get_dict()['$regex'] = regex
        if opts: self.__get_dict()['$options'] = opts
        return self

    def STARTSWITH(self, string):
        return self.RE('^' + string)

    def __repr__(self):
        """This is just to make ipython/pprint happy"""
        return dict.__repr__(self)
        
class MagicFactory(object):
    def __getattribute__(self, name):
        return Magic(name)

M = MagicFactory()

def AND(*args):
    d = {}
    for arg in args:
        d.update(arg)
    return d

if __name__ == '__main__':
    import doctest
    doctest.testfile("README")

