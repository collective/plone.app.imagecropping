from plone.app.imagecropping.storage import Storage
from Products.Five.browser import BrowserView


class CroppingView(BrowserView):
    DEFAULT_FORMAT = "PNG"

    def __call__(self, **kw):
        form = self.request.form
        fieldname = form["fieldname"]
        scale_id = form["scale"]
        if "remove" in form:
            storage = Storage(self.context)
            storage.remove(fieldname, scale_id)
            return "OK"

        box = (
            int(round(float(form["x"]))),
            int(round(float(form["y"]))),
            int(round(float(form["x"]) + float(form["width"]))),
            int(round(float(form["y"]) + float(form["height"]))),
        )
        self._crop(fieldname, scale_id, box)
        return "OK"

    def _crop(self, fieldname, scale, box):
        """Delegate to store."""
        storage = Storage(self.context)
        storage.store(fieldname, scale, box)
