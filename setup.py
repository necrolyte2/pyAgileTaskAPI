import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def scripts( ):
    return [os.path.join( 'bin', f ) for f in os.listdir( 'bin' )]

# The next three lines are modified from Biopython
__version__ = "Undefined"
for line in open('agiletaskapi/__init__.py'):
    if (line.startswith('__version__')):
        exec(line.strip())
        break

setup(
    name = "pyAgileTaskAPI",
    version = __version__,
    author = "Tyghe Vallard",
    author_email = "vallardt@gmail.com",
    description = ("AgileTask API bindings implemented in python"),
    keywords = "AgileTask api python bindings wrapper",
    url = "https://github.com/necrolyte2/pyAgileTaskAPI",
    packages = ['agiletaskapi'],
    #scripts = scripts(),
    data_files = [
    ],
    install_requires = [
    ],
    long_description=read('README.markdown'),
)
