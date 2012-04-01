#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, home, admin

url_patterns = [
    ("/", home.HomePageHandler),
    ("/vote", home.HomePageHandler),
    ##########ADMIN HANDLERS#################
    ("/populate", admin.PopulateDummyHandler),
]
