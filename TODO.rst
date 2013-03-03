spread the word
===============

xxx mention this package on:

* http://stackoverflow.com/questions/11241031/cropping-images-instead-of-scaling-with-plone-and-archetypes
* your planet-plone-blog
* tweet
* upload to pypi
* product page on plone.org
* the plip: http://dev.plone.org/plone/ticket/10174
* inform author of branch https://github.com/plone/plone.app.imaging/tree/ggozad-cropping
* inform people that attended the openspace (frisi has adresses)


FIXME
=====

test_accessing_images fails when accessing the scale via @@images

TinyMCE
-------

If an image scale is added to TinyMCE it gets transformed to its uid
representation (as stored in plone.scale.storage).
If the cropped scale gets removed the uid does not exists anymore and
the referenced image in TinyMCE raises NotFound exception.


Implementation
==============



Cropping view
-------------


**2 possible approaches**

a) show a preview image for every scale with a link to choose cropping area with the editor
b) show a dropdown with available scales, picture below

b) preferred, more user friendly, not necessary to show a list of all scaled images (faster)


The view has to care about all image fields defined on the context (for archetypes it's just iterating over the schema, dexterity iterates over all behaviours).
Just one field: editor shows image directly.
More fields: page to select image, editor on next page or in an overlay.
even better: show the firs, have other in a preview column (think tabbed view)


**Possible editor problems**

* how to only store crops for scales the user really cared about
  (extra apply button that just saves the currently edited scale)

* shown full resolution image might be slow
  configurable size for the preview might be a good idea
  but showing downscaled version limits user in terms of precision of selecting a certain precise part of an image

* removing scales has to be possible too

* read cropping information from the field to mark the correct area if opened for an already cropped scale

* tiny support:
  the user should be able to change the crop via a link just below
  the image scale selection in Tiny image plugin (could open a crop-editor in an overlay)
  chosen scale selected as active one in the editor (others should not be available).
  a toolbar button might be less work and we would not need to path/replace
  the existing image plugin



**Class croppingview**

#this is used to display in JCrop
INITIAL_SIZE = (1000,1000)

@property
def available_scales()
{'fieldname1': {'scales': [('preview', 200, 200)],
                 'thumb': 'we might use that in case multiple fields are there',
                 'truesize' (5000,3450),
                 'preview': 'picture url resized to INITIALSIZE to use in JCrop',
                 'interface': 'optional.Interface',
               },
}





This allows you to select a certain scale

It fires up the cropping editor with the aspect ratio fixed to the ratio of the chosen scale.
In case of a tile(16,16) the ratio would be 1:1.

Apply button:
We are going to store the cropped and resized version of the image as the plone.app.imaging traverser would do when we first access the image.




plone.app.imagetransforms
=========================

in bristol we have been talking about grayscale, sepia, watermark transforms
and wanted to add this to p.a.imaging.

these functionalities will go into a separate addon.

chaining transforms shall be possible



for the integrator::


  scales img/@@images
  scales.scale('imagefield', scale='mini').apply('grayscale', 0.5).apply('watermark', text='mycopyright')

  #and even nicer:
  scales.scale('imagefield', scale='mini').grayscale(0.5)



