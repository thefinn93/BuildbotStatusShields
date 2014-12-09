#!/usr/bin/env python
import os
from setuptools import setup


def readme(fname):
    md = open(os.path.join(os.path.dirname(__file__), fname)).read()
    output = md
    try:
        import pypandoc
        output = pypandoc.convert(md, 'rst', format='md')
    except ImportError:
        pass
    return output

setup(
    name="BuildbotEightStatusShields",
    version="0.1",
    author="Finn Herzfeld",
    author_email="finn@finn.io",
    description=("Adds shields.io-style badges to Buildbot"),
    license = "GPLv2",
    keywords = "shields badges status Buildbot",
    url = "https://github.com/thefinn93/BuildbotStatusShields",
    packages=['BuildbotStatusShields'],
    long_description=readme('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha"
    ],
    install_requires=['CairoSVG', 'cairocffi', 'Jinja2'],
    package_data={
        'BuildbotStatusShields': ['templates/*.svg.j2']
    },
    include_package_data = True
)
