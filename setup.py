#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.26.0',
    'requests_downloader>=0.2.3',
    'beautifulsoup4>=4.10.0',
    'lxml>=4.6.2',
    'peewee>=3.14.4',
    'indic_transliteration>=2.2.4',
]

test_requirements = ['pytest>=3', ]

setup(
    author="Hrishikesh Terdalkar",
    author_email='hrishikeshrt@linuxmail.org',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Access various dictionaries from CDSL (Cologne Digital Sanskrit Lexicon)",
    entry_points={
        'console_scripts': [
            'cdsl=pycdsl.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['pycdsl', 'sanskrit', 'lexicon', 'dictionary'],
    name='PyCDSL',
    packages=find_packages(include=['pycdsl', 'pycdsl.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hrishikeshrt/PyCDSL',
    version='0.2.0',
    zip_safe=False,
)
