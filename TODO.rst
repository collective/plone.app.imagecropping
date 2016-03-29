the follwoing needs checks if its still valid.
if yes make it an github issue, if no remove from here:

FIXME
=====

test_accessing_images fails when accessing the scale via @@images

TinyMCE
-------

If an image scale is added to TinyMCE it gets transformed to its uid
representation (as stored in plone.scale.storage).
If the cropped scale gets removed the uid does not exists anymore and
the referenced image in TinyMCE raises NotFound exception.


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
