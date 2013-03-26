from setuptools import setup, find_packages
import os

version = '0.1rc2.dev0'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='plone.app.imagecropping',
      version=version,
      description=\
        "allows images to be manually cropped using JCrop JS library",
      long_description=long_description,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
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
          'setuptools',
          'Pillow',
          'plone.app.imaging',
          'Products.ATContentTypes',
          'Products.CMFPlone>=4.1'
      ],
      extras_require={
          'test': [
              'lxml',
              'plone.app.testing',
              'robotsuite',
              'robotframework-selenium2library',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
