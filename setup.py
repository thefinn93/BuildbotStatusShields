#!/usr/bin/env python
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="BuildbotStatusShields",
    version="0.1",
    author="Finn Herzfeld",
    author_email="finn@finn.io",
    description=("Adds shields.io-style badges to Buildbot"),
    license = "GPLv2",
    keywords = "shields badges status buildbot",
    url = "https://github.com/thefinn93/BuildbotStatusShields",
    packages=['BuildbotStatusShields'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha"
    ],
    install_requires=['CairoSVG', 'cairocffi', 'Jinja2']
)
