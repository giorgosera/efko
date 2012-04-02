from app.handlers import base
from app.model.video import *

class TermsHandler(base.BaseHandler):

    def on_get(self):
        self.base_render("terms.html")

class PrivacyHandler(base.BaseHandler):

    def on_get(self):
        self.base_render("privacy.html")
    