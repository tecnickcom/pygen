"""Packaging settings."""


from codecs import open
from os.path import dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from ~#PROJECT#~ import __version__ as VERSION


def read(fname):
    return open(join(dirname(__file__), fname)).read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call([
            'py.test',
            '--verbose',
            '--cov=~#PROJECT#~',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ])
        raise SystemExit(errno)


setup(
    name='~#PROJECT#~',
    version=VERSION,
    description='~#SHORTDESCRIPTION#~',
    long_description=read('README.md'),
    url='~#PROJECTLINK#~',
    author='~#OWNER#~',
    author_email='~#OWNEREMAIL#~',
    license='~#LICENSE#~',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: ~#LICENSE#~',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='~#PROJECT#~',
    packages=find_packages(exclude=['docs', 'tests*']),
    data_files=[
        ('config', ['resources/etc/~#PROJECT#~/config.json', 'resources/etc/~#PROJECT#~/config.schema.json']),
        ('info', ['VERSION', 'RELEASE', 'LICENSE', 'README.md'])
    ],
    install_requires=[
        'docopt',
        'python-json-logger',
        'structlog',
        'statsd',
        'ujson',
        'requests',
        'werkzeug',
    ],
    extras_require={
        'test': [
            'coverage',
            'pytest',
            'pytest-benchmark',
            'pytest-cov',
            'pytest-pep8',
        ],
    },
    entry_points={
        'console_scripts': [
            '~#PROJECT#~=~#PROJECT#~.__main__:main',
        ],
    },
    cmdclass={'test': RunTests},
)
