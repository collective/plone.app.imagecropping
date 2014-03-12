from setuptools import setup, find_packages

version = '0.1rc3.dev0'

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
      description="Allows images to be manually cropped using JCrop JS library",
      long_description=long_description,
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
          'Acquisition',
          'Pillow',
          'plone.app.blob',
          'plone.app.imaging',
          'plone.app.registry',
          'plone.behavior',
          'plone.namedfile [blobs]',
          'plone.registry',
          'plone.scale',
          'Products.ATContentTypes',
          'Products.CMFCore',
          'Products.CMFPlone >=4.2'
          'Products.GenericSetup',
          'Products.statusmessages',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.dexterity',
              'plone.app.testing [robot] >=4.2.2',
              'plone.testing',
              'robotsuite',
              'transaction',
              'unittest2',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
