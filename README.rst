.. image:: https://travis-ci.org/collective/plone.app.imagecropping.png?branch=master
    :target: http://travis-ci.org/collective/plone.app.imagecropping

.. image:: https://coveralls.io/repos/collective/plone.app.imagecropping/badge.png
    :target: https://coveralls.io/r/collective/plone.app.imagecropping

.. contents::


Why do I need this?
===================

Automatic cropping is already possible, `plone.app.imaging`_ does already handle this via the ``direction`` parameter::

  <img tal:define="scales context/@@images"
       tal:replace="structure python: scales.tag('image',
                    width=1200, height=800, direction='down')"
       />

However it only crops from the top/center of the image,
so in some ocasions this is not what you want.

``plone.app.imagecropping`` allows you to select the cropping area manually for each available image scale using the `cropper`_  Javascript library

.. _`plone.app.imaging`: http://pypi.python.org/pypi/plone.app.imaging
.. _`cropper`: https://github.com/fengyuanchen/cropper


How it works
============

There is a view @@croppingeditor available for every content type implementing ``IImageCroppingMarker`` via an object action. There are specific markers for Archetypes and Dexterity based types:

- ``plone.app.imagecropping.dx.IImageCroppingDX``
- ``plone.app.imagecropping.at.IImageCroppingAT``

The interfaces are implemented by default for Dexterity based ``plone.app.contenttypes`` (Plone 5 or Plone 4.x as addon) ``Image``.
``Products.ATContentTypes`` (Plone 4.x) implements it on``ATImage`` and ``ATNewsItem``.

There is also a Dexterity behavior called ``Enable Image Cropping`` which can be applied on custom content types containing at least one image.

The editor view hav a tabbed navigation on the top and two columns:

- Image fields on tabbed navigation.
- Image scales column on left
- Cropping editor column on right.

The aspect ratio for the cropping area in the editor is automatically set to the image scale selected by the user.

.. image:: https://raw.github.com/collective/plone.app.imagecropping/master/docs/editor.png

The image stored for this scale gets replaced with the cropped and scaled version.
This way you can access them as you're used to. For example::

  <img tal:replace="structure context/@@images/image/mini" />

This also enables support for richtext editors such as TinyMCE to insert cropped scales into a textfield.


Automatic cropping behavior
---------------------------

You can use ``direction='down'`` for autocropped scales as usual.
This package overrides the direction and delivers the cropped scale if it is available.


Load editor as overlay
----------------------

The editor can also be loaded as an overlay anywhere.
Just place a link to the ``@@croppingeditor`` url of an image (``<image_base_url>/@@croppingeditor``) and add some javascript. For example::

    (function($) {
        $(function() {
            $("a[href$='@@croppingeditor']").prepOverlay({
                subtype:'ajax',
                formselector:'#coords',
                closeselector:"input[name='form.button.Cancel']"
            })

            $(document).bind("formOverlayLoadSuccess", function() {
                imagecropping = new ImageCropping();
                imagecropping.init_editor();
            })
        })
    })(jQuery);

TODO: Show how to use with mockup/patterns.

Configuration
-------------

At ``Plone Site Setup`` under ``Content`` there is a new setting ``Image Cropping``.
There you can limit the scales to be shown in the cropping editor.
By default all scales are shown.

You can also set those values in the profile of your (policy)product using
``plone.app.registry`` mechanism (file ``registry.xml``).


Further Information
===================

History
-------

There has been a need for cropping for a long time and there are lots of addons around that have different ways to achieve this.

There is `plip #10174`_ asking for adding image cropping to plone core which recently got rejected by the FWT.
The cropping functionality should go into an addon first that also work for dexterity and can be pliped into core.

.. _`plip #10174`: http://dev.plone.org/plone/ticket/10174

This package aims to be THE cropping solution for plone that 'just works TM'.


Design decisions
----------------

* make this package as minimally invasive as possible

  - therefore we store the cropped image immediately, so plone.app.imaging
    traverser doesn't need to care about cropping

  - users can access cropped images the same way as the access scales
    (so it works in richtext editors too)

* support archetypes and dexterity content

* a cropped image gets stored instead of the scaled image.
  if you want back the uncropped image scale you'll need to remove the cropped version
  in the editor


Information about changes from version 1.x to 2.0
-------------------------------------------------

- Plone 5.1 only.
- New js library `cropper`_.
- Complete Javascript rewrite using patterns.
- New editor layout.
- Save/Remove using Ajax.

Information about changes from version 0.1 to 1.0
-------------------------------------------------

The marker interface for archetypes changed from
``plone.app.imagecropping.interfaces.IImageCropping`` to
``plone.app.imagecropping.at.IImageCroppingAT``.

The marker interface for dexterity based types changed from
``plone.app.imagecropping.browser.scaling.interfaces.IImageCroppingScale`` to
``plone.app.imagecropping.dx.IImageCroppingDX``.

The generic base interface is now
``plone.app.imagecropping.interfaces.IImageCroppingMarker``.
Do not use it directly on your, but use the marker to bind view or other adapters to image-cropping enabled types.


Possible extensions / changes for the future
--------------------------------------------

* allow to mark scales as `auto-croppable` in the plone.app.imaging controlpanel.
  this enables cropped scales w/o manually defining the cropping area but would require some changes in plone.app.imaging
  (extend traverser, change controlpanel)

* see also the `issue tracker <https://github.com/collective/plone.app.imagecropping/issues>`_
