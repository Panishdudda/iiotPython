from setuptools import setup

VERSION = '0.1' 
DESCRIPTION = 'CNC Machine Signals COllection package'
LONG_DESCRIPTION = 'This package helps in collecting signals from cnc machine and store in local db'

#setup
setup(
        name="signal_package", 
        version=VERSION,
        author="Gautam Patil",
        author_email="gautampatil728gp4@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        install_requires=[], # no dependencies required for use of this package


)