#i want to be able to masquerade these drivers under the clusto. namespace!
#http://docs.python.org/tutorial/modules.html#packages-in-multiple-directories
#http://smallpy.posterous.com/python-import-magic-python-package-over-multi
#http://www.travisswicegood.com/2009/12/22/the-problem-with-python-namespaces-modul/
#http://www.python.org/dev/peps/pep-0382/
#http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages hmm, you can't go multiway on the top-level 'clusto' name. fuuuuu...

#okay, just implement a custom loader whenever *clusto* is searched. geez. http://orestis.gr/blog/2008/12/20/python-import-hooks/

'''
#http://bitbucket.org/ianb/paste/src/tip/paste/__init__.py
# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    # don't prevent use of paste if pkg_resources isn't installed
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__) 

try:
    import modulefinder
except ImportError:
    pass
else:
    for p in __path__:
        print p
        print __name__
        modulefinder.AddPackagePath(__name__, p)
'''
from . import drivers
