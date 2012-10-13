from Products.Five.browser import BrowserView


class CroppingEditor(BrowserView):

    #this is used to display in JCrop
    INITIAL_SIZE = (1000,1000)

    @property
    def available_scales(self)
        """returns information to initialize JCrop for all available fields on
        the current context
        """

#    {'fieldname1': {'scales': [('preview', 200, 200)],
#                     'thumb': 'we might use that in case multiple fields are there',
#                     'truesize' (5000,3450),
#                     'preview': 'picture url resized to INITIALSIZE to use in JCrop'}}


