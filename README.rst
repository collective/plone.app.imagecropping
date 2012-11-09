.. contents::


History
=======

There has been a need for cropping for a long time and there are lots of addons around
that have different ways to achieve this.

There is `plip #10174`_ asking for adding image cropping to plone core
which recently got rejected by the FWT. The cropping functionality should go
into an addon first that also work for dexterity and can be pliped into core.

.. _`plip #10174`: http://dev.plone.org/plone/ticket/10174

This package aims to be THE cropping solution for plone that `just works TM`.


Why do I need this?
===================

Automatic cropping is already possible, `plone.app.imaging`_ does already handle this
via the ``direction`` parameter::

  <img tal:define="scales context/@@images"
       tal:replace="structure python: scales.tag('image',
                    width=1200, height=800, direction='down')"
       />

However it only crops from the center of the image,
so in some ocasions this is not what you want.

``plone.app.imagecropping`` allows you to select the cropping area manually
for each available image scale using the `JCrop editor`_

.. _`plone.app.imaging`: http://pypi.python.org/pypi/plone.app.imaging
.. _`JCrop editor`: http://deepliquid.com/content/Jcrop.html


How it works
============

There is a view @@croppingeditor available for every content type
implementing ``IImageCropping`` via an object action.

The Interface is implemented by default for ATImage XXX and plone.app.contenttypes image.


The view shows a dropdown for all available image scales.
The aspect ratio for the cropping area in JCrop editor is automatically set
to the image scale selected by the user.

.. image:: https://raw.github.com/collective/plone.app.imagecropping/master/docs/editor.png

The image stored for this scale gets replaced with the cropped and scaled version.
This way you can access them as you're used to. For example::

  <img tal:replace="structure context/@@images/image/mini" />

This also enables support for richtext editors such as TinyMCE to insert
cropped scales into a textfield.

In TinyMCE it will be possible to access the cropping editor directly
out of the image plugin right below the scale selection

Configuration
-------------

A Configlet is registered in Plone Site Setup. There you can adjust the
maximum Size of the jCrop Editor Image (large_size) and the minimum selectable
size of the cropped area (min_size).

You can also set those values in the profile of your (policy)product using
p.a.registry mechanism (registry.xml)::

  <registry>
    <records interface="plone.app.imagecropping.browser.settings.ISettings">
        <value key="large_size">500:500</value>
        <value key="min_size">10:10</value>
    </records>
  </registry>


Design decisions
----------------

* make this package as minimally invasive as possible

  - therefore we store the cropped image immediately, so plone.app.imaging
    traverser doesn't need to care about cropping

  - users can access cropped images the same way as the access scales
    (so it works in richtext editors too)

* support archetypes and dexterity content
  (XXX limitation for dexterity: this will only work for images in AttributeStorage)

* a cropped image gets stored instead of the scaled image.
  if you want back the uncropped image scale you'll need to remove the cropped version
  in the editor





Possible extensions / changes for the future
--------------------------------------------

* allow to mark scales as `auto-croppable` in the plone.app.imaging controlpanel.
  this enables cropped scales w/o manually defining the cropping area
  but would require some changes in plone.app.imaging (extend traverser, change
  controlpanel)




