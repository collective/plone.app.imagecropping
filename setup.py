from setuptools import setup

version = "4.0.1.dev0"

setup(
    name="plone.app.imagecropping",
    version=version,
    description="Crops Images in Plone manually using cropper JS library",
    long_description="\n\n".join(
        [
            open("README.rst").read(),
            open("CONTRIBUTORS.rst").read(),
            open("CHANGES.rst").read(),
        ]
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone image crop",
    author="Plone Collective",
    author_email="plone-developers@lists.sourceforge.net",
    project_urls={
        "Homepage": "https://github.com/collective/plone.app.imagecropping",
    },
    license_expression="GPL-2.0-or-later",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "Pillow",
        "plone.app.dexterity",
        "plone.app.registry",
        "plone.base",
        "plone.behavior",
        "plone.dexterity",
        "plone.namedfile>=6.0.0",
        "plone.registry",
        "plone.scale",
        "plone.z3cform",
        "Products.CMFCore",
        "Products.GenericSetup",
        "z3c.caching",
        "z3c.form",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.api",
            "plone.app.contenttypes",
            "plone.app.testing",
            "plone.app.robotframework[debug]",
            "plone.browserlayer",
            "plone.testing",
            "robotsuite",
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
