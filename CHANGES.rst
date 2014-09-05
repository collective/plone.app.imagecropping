Changelog
=========

1.0 (2014-09-05)
----------------

- fixed jcrop image to not scale wrong (!). 
  [jensens]

- better initial selection for cropping, also mark scales in left column 
  cropped/ uncropped and show uncropped in its default appereance.
  [jensens]

- Fix: Removed registration of Traverse for dexterity types since its
  base class does not support dexterity either.
  [jensens]

- Added subscriber to recreate all scales on copied objects.
  [saily, jensens]

- fixed some glitches in JCrop init process.
  [jensens]

- added dexterity behavior for image cropping.
  [benniboy]

- Major cleanup and split up code and interfaces into Dexterity and Archtypes.
  Also renamed/ moved Interfaces to be used as markers! Attention, in custom
  code minor changes are needed in order to point to the correct interfaces.
  see README for details.
  Also removed some superfluos/unused ``interface=`` passes to methods of
  ``IImageCroppingUtils``.
  [jensens]

- Update Jcrop to version 0.9.12.
  [hvelarde]

- Use ``plone.app.robotframework`` instead of writing all keywords from
  scratch. This brings us autologin support for faster robot tests. Rewrite
  tests to test scenarios.
  [saily]

- Drop Plone 4.1 support and tests.
  [saily]

- Cleanup code, align to all coding conventions for Plone.
  Pep8, Flake8, pep3101, sort imports, remove grouped imports, ...
  [saily]

- Cleanup/refactor javascript code, don't define global variables.
  [saily]

- Add coveralls, code-analysis and update travis configuration.
  [saily]

- Check for plone.namedfile not Dexterity. It can be used seperately.
  *If plone.namedfile is used it needs to be at least version 2.0.1*
  [tomgross]

- ``@@croppingeditor`` now displays a message to add croppable scales
  in the controlpanel if there are no croppable scales to show.
  (previously this caused a `SiteError`)
  [fRiSi]

- Rename ``imagecropping_keywords.txt`` to ``keywords.robot`` to allow simple
  reusage in ``plone.app.robotframework``.
  [saily]

- pin zc.buildout=2.1.1 for travis-ci boostrap
  [petschki]

- Added Russian translations
  [bogdangi]

- Prevent fieldname loosing for for current field
  [bogdangi]

- Fixed #21 (cropping was reset on modifying image)
  [tomgross, fRiSi]

- Only test Plone 4.2 and 4.3 with Python 2.7 on Travis-CI
  [tomgross]

0.1rc2 (2013-05-03)
-------------------

- Include styles for authenticated users only.
  [saily]

- Make tests work in Plone 4.1
  [saily]

- Rename *acceptance* to *robot* to align new
  ``plone.app.robotframework`` guidelines.
  [saily]

- Pin ``plone.app.testing`` to make Plone 4.1 tests work.
  [saily]

- Use correct dependency for plone.app.testing with extra ``[robot]``.
  [saily]

- Add cropping ui-tests using robotframework
  [saily]

- Update ``bootstrap.py`` to work with ``zc.buildout`` 2.0
  [saily]

- Implemented #11 - Mark image scales as "croppable"
  [jensens]

- Added tests for control panel and registry
- Added Spanish and Brazilian Portuguese translations
  [hvelarde]

- Small documentation update
  [saily]


0.1rc1 (2013-03-11)
-------------------

- add support for multiple image fields
- refactored javascript includes so the editor can be loaded as overlay
- fixed JS error when editor is invisible (ie editor is loaded in an overlay)
- fixed edit/remove actions when editor is loaded as overlay
- make editor view more convenient (disable columns)
- update documentation
  [petschki]

0.1b1 (2013-03-03)
------------------

- Made cropping work in dexterity-only sites
  [pysailor]

- Add travis integration
  [saily]


0.1a2 (2012-11-10)
------------------

- fix tests
- add test setups for Plone 4.1-4.3
- Products.CMFPlone dependency. Right now we only support Plone >= 4.1
- make dexterity support optional
  [petschki]


0.1a1 (2012-11-05)
------------------

- public alpha release
  [petschki]
- Package created using templer
  [fRiSi]
