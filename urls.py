#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, home, admin, rankings

url_patterns = [
    ("/", home.HomePageHandler),
    ("/next", home.HomePageHandler),
    ("/vote", home.VoteHandler),
    ("/rankings", rankings.ViewRankingsHandler),
    ("/submit", home.SubmitCoverHandler),
    ##########ADMIN HANDLERS#################
    ("/populate", admin.PopulateDummyHandler),
]
