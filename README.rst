.. contents::

Introduction
============


aim
----

There has been a need for cropping and there are lots of addons and a plip too:
http://dev.plone.org/plone/ticket/10174

this package meant to be THE cropping solution for plone that just works TM


why would you want/need this addon.
automatic cropping already possible. but sometimes not what you want
eg example image for crop problem



explain how to define crop areas should be outlined here
xxx very important ;-)



design decisions

* store the cropped image immediately, so p.a.i traverser need not care about cropping
  xxx this might be changed when this goes into core
* need not patch/overwrite/change default imaging behaviour in plone
* crop gets stored as scaled image. no way to access just the resized scale unless cropinfo gets removed


let user define crop region manually in case the automatic behaviour leads to an unwanted result
xxx example image



use cases we want to support

* support archetypes imagefield (custom content type and atctimage, think collective.contentleadimage) and dexterity content
  XXX limitation: this will only work for images in attributestorage

* user uploads new image or referres existing one in tinymce.
  should be able to change crop via a link just below the image scale selection in tiny image plugin (could open crop-editor in an overlay)






implementation:
===============

cropping view
-------------


2 possible approaches:

a) show preview image for every scale with link to choose cropping region with editor
b) show dropdown with available scales, picture below

b) preferred, more user friendly, not necessary to show a list of all scaled images (faster)


view has to care about all image fields defined on the context (for archetypes it's just iterating over the schema, dexterity iterate over all behaviours)
just one field: editor shows image direclty
more fields: page to select image, editor on next page or in an overlay


possible editor problems:

* how to only store crops for scales the user really cared about
  (extra apply button that just saves the currently edited scale)

* shown full resolution image might be slow.
  configurable size for the preview might be a good idea
  but showing downscaled version limits user in terms of precision of selecting a certain

* removing scales should be possible too

* read cropping information from the field to mark the correct area if opened for an already cropped scale



for archetypes and dexterity (by adding the interface option) this should kinda work:
contextobject/@@storeCrop?interface=my.package.foo.interfaces.IInterface&fieldname=image&scalename=thumb,crop-information



class croppingview:

#this is used to display in JCrop
INITIAL_SIZE = (1000,1000)

@property
def available_scales()
{'fieldname1': {'scales': [('preview', 200, 200)],
                 'thumb': 'we might use that in case multiple fields are there',
                 'truesize' (5000,3450),
                 'preview': 'picture url resized to INITIALSIZE to use in JCrop'}}





allows to select a certain scale

fires up cropping editor with the aspect ratio fixed to the ratio of the chosen scale.
in case of tile(16,16) ratio would be 1:1

apply button:
we gonna store the cropped and resized version of the image as the p.a.i traverser would do when we first access the image





use cropped version as you are used to use the scales::

type/imagefieldname_scale
xxx refere to p.a.i documentation or show examples here


plone.app.imagetransforms



mention other transforms and how they could be implemented (most probably in a different new addon)