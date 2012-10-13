.. contents::


Goal
====

There has been a need for cropping for a long time and there are lots of addons around
that have different ways to achieve this.

There is `plip #10174`_ asking for adding image cropping to plone core
which recently got rejected by the FWT. The cropping functionality should go
into an addon first that also work for dexterity and can be pliped into core.

.. _`plip #10174`: http://dev.plone.org/plone/ticket/10174

This package aims to be THE cropping solution for plone that `just works TM`.


Why would you want/need this addon
----------------------------------

Automatic cropping is already possible, ``plone.app.imaging`` does already handle this
via the ``direction`` parameter::

  <img tal:define="scales context/@@images"
       tal:replace="structure python: scales.tag('image',
                    width=1200, height=800, direction='down')"
       />

However it only crops from the center of the image,
so in some ocasions this is not what you want.

``plone.app.imagecropping`` allows you to select the cropping area yourself.


How it works
============

There is a view @@


<img tal:replace="structure context/@@images/image/mini" />


*explain how to define crop areas should be outlined here
xxx very important ;-)*


xxx mention this is based on https://github.com/plone/plone.app.imaging/tree/ggozad-cropping


Design decisions
----------------

* we need to store the cropped image immediately, so plone.app.imaging traverser doesn't need to care about cropping
  xxx this might be changed when this goes into core
* need not patch/overwrite/change default imaging behaviour in plone
* a cropped image gets stored as scaled image. there is no way to access the resized scale unless cropinfo gets removed


A user should be able to define the cropping area manually in case the automatic behaviour leads to an unwanted result.
*xxx example image*



**Use cases we want to support**

* support archetypes imagefield (custom content type and atctimage, think collective.contentleadimage) and dexterity content
  XXX limitation: this will only work for images in attributestorage

* a user uploads a new image or referrers an existing one in TinyMCE.
  the user should be able to change the crop via a link just below the image scale selection in Tiny image plugin (could open a crop-editor in an overlay)






Implementation
===============

Cropping view
-------------


**2 possible approaches**

a) show a preview image for every scale with a link to choose cropping area with the editor
b) show a dropdown with available scales, picture below

b) preferred, more user friendly, not necessary to show a list of all scaled images (faster)


The view has to care about all image fields defined on the context (for archetypes it's just iterating over the schema, dexterity iterates over all behaviours).
Just one field: editor shows image directly.
More fields: page to select image, editor on next page or in an overlay.


**Possible editor problems**

* how to only store crops for scales the user really cared about
  (extra apply button that just saves the currently edited scale)

* shown full resolution image might be slow
  configurable size for the preview might be a good idea
  but showing downscaled version limits user in terms of precision of selecting a certain precise part of an image

* removing scales should be possible too

* read cropping information from the field to mark the correct area if opened for an already cropped scale



For archetypes and dexterity (by adding the interface option) this should kinda work:
contextobject/@@storeCrop?interface=my.package.foo.interfaces.IInterface&fieldname=image&scalename=thumb,crop-information



**Class croppingview**

#this is used to display in JCrop
INITIAL_SIZE = (1000,1000)

@property
def available_scales()
{'fieldname1': {'scales': [('preview', 200, 200)],
                 'thumb': 'we might use that in case multiple fields are there',
                 'truesize' (5000,3450),
                 'preview': 'picture url resized to INITIALSIZE to use in JCrop'}}





This allows you to select a certain scale

It fires up the cropping editor with the aspect ratio fixed to the ratio of the chosen scale.
In case of a tile(16,16) the ratio would be 1:1.

Apply button:
We are going to store the cropped and resized version of the image as the plone.app.imaging traverser would do when we first access the image.





Use the cropped version as you are used to use the scales:

type/imagefieldname_scale
*xxx refer to plone.app.imaging documentation or show examples here*


*plone.app.imagetransforms*



*We should mention other transforms and how they could be implemented (most probably in a different new addon)*



xxx mention this package on http://stackoverflow.com/questions/11241031/cropping-images-instead-of-scaling-with-plone-and-archetypes
