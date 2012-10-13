from Products.Five.browser import BrowserView


class CroppingView(BrowserView):

    def __call__(self, **kw):
        return "worked"

    #for archetypes and dexterity (by adding the interface option) this should kinda work:
    #contextobject/@@storeCrop?interface=my.package.foo.interfaces.IInterface&fieldname=image&scalename=thumb,crop-information


    def _crop(self, parms, here):
        pass