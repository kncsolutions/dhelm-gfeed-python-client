from setuptools import setup, find_packages
from codecs import open
from os import path
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

here = path.abspath(path.dirname(__file__))
with open("README.rst", "r") as f:
    long_description = f.read()

name = 'DhelmGfeedClient'
version = '1.0.1'
release = '1.0.1'
copyright = '2018, KNC Solutions Private Limited.'
setup(
    name=name,
    version=release,
    packages=find_packages(exclude=['build', 'docs', 'example']),
    cmdclass=cmdclass,
    url='https://github.com/kncsolutions/dhelm-gfeed-python-client',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.4',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    author='Pallav Nandi Chaudhuri',
    author_email='developer@kncsolutions.in',
    description='This is a python client for websocket APIs provided by Global Financial Datafeeds LLP to access financial data.',
    copyright=copyright,
    long_description=long_description,
    install_requires=[
        "autobahn[twisted]>=18.9.2"
    ],
    extras_require={
        "doc": ["Sphinx"],
    },
     project_urls={  # Optional
        'Bug Reports': 'https://github.com/kncsolutions/dhelm-gfeed-python-client/issues',
        'Source': 'https://github.com/kncsolutions/dhelm-gfeed-python-client',
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', 'docs/_build'),
            'copyright' : ('setup.py', copyright)}},
)
