# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.3-dev0'

setup(
    name='plone.app.imagecropping',
    version=version,
    description="allows images to be manually cropped using JCrop JS library",
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('CONTRIBUTORS.rst').read(),
        open('CHANGES.rst').read(),
    ]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone image crop',
    author='',
    author_email='',
    url='https://github.com/collective/plone.app.imagecropping',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition',
        'Pillow',
        'plone.app.blob',
        'plone.app.imaging',
        'plone.app.registry',
        'plone.behavior',
        'plone.namedfile>=2.0.1',
        'plone.registry',
        'plone.scale',
        'Products.CMFCore',
        'Products.CMFPlone>=4.2'
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.globalrequest',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
        'z3c.caching',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.dexterity',
            'plone.app.robotframework',
            'plone.app.testing[robot]>=4.2.2',
            'plone.testing',
            'robotsuite',
            'zope.event',
        ],
        'archetypes': [
            'Products.ATContentTypes',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
