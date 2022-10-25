# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '3.0.0'

setup(
    name='plone.app.imagecropping',
    version=version,
    description='Crops Images in Plone manually using cropper JS library',
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('CONTRIBUTORS.rst').read(),
        open('CHANGES.rst').read(),
    ]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: Addon',
        'Framework :: Plone :: 6.0',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone image crop',
    author='Plone Collective',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/collective/plone.app.imagecropping',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFPlone>=6.0b3',  # Module Federation support
        'plone.namedfile>=6.0.0b5',
        'setuptools',
        'six',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
