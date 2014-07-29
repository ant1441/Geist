from __future__ import division
from keyword import kwlist
import glob
import os
import os.path
import re

import numpy

from .finders import BaseFinder


VALID_NAME = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')

class Template(object):
    def __init__(self, image, name, repo):
        self.image = image
        self.name = name
        self.repo = repo

    def __repr__(self):
        return "template %r in repo %r" % (self.name, self.repo)


class DirectoryRepo(object):
    def __init__(self, directory):
        self.__directory = os.path.abspath(directory)
        self.__ensure_dir_exists()

    def __ensure_dir_exists(self):
        try:
            os.makedirs(self.__directory)
        except:
            pass

    def _valid_name(self, name):
        """
        Check this is a valid name, otherwise we might have issues later
        """
        if VALID_NAME.match(name) is None:
            return False
        if name in kwlist:
            return False
        return True

    def __getitem__(self, key):
        self.__ensure_dir_exists()
        imgpath = os.path.join(self.__directory, key + '.npy')
        if os.path.exists(imgpath):
            return Template(numpy.load(imgpath), name=key, repo=self)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.__ensure_dir_exists()
        if not self._valid_name(key):
            raise NameError(key)
        if type(value) is numpy.ndarray:
            numpy.save(os.path.join(self.__directory, key + '.npy'), value)
        else:
            raise ValueError('type not supported: %s' % (type(value),))

    def __delitem__(self, key):
        self.__ensure_dir_exists()
        imgpath = os.path.join(self.__directory, key + '.npy')
        if os.path.exists(imgpath):
            os.remove(imgpath)
        else:
            raise KeyError(key)

    @property
    def entries(self):
        return list(self)

    def __iter__(self):
        return iter(os.path.split(i)[1].rsplit('.', 1)[0] for i in
                    glob.glob(os.path.join(self.__directory, '*.npy')))

    def __repr__(self):
        return "directory repo %r" % (self.__directory, )


class TemplateBasedFinder(BaseFinder):
    def __init__(self, repo, name, finder_constructor):
        self._name = name
        self._repo = repo
        self._finder_constructor = finder_constructor

    def find(self, in_location):
        for loc in self._finder_constructor(self._repo[self._name]).find(
            in_location
        ):
            yield loc

    def __repr__(self):
        return "%s finder for %r" % (self._finder_constructor, self._name)


class TemplateFinderFromRepo(object):
    def __init__(self, repo, finder_constructor):
        self._repo = repo
        self._finder_constructor = finder_constructor

    def __dir__(self):
        return self._repo.entries

    def __getattr__(self, name):
        return TemplateBasedFinder(self._repo, name, self._finder_constructor)
