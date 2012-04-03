#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, home, admin, rankings, landing, user

url_patterns = [
    ("/", home.HomePageHandler),
    ("/welcome", home.WelcomePageHandler),
    ("/next", home.HomePageHandler),
    ("/vote", home.VoteHandler),
    ("/rankings", rankings.ViewRankingsHandler),
    ("/submit", home.SubmitCoverHandler),
    ##########LANDING HANDLERS#################
    ("/terms", landing.TermsHandler),
    ("/privacy", landing.PrivacyHandler),
    ("/about", landing.AboutHandler),   
    ##########ADMIN HANDLERS#################
    ("/thisisasecreturl18211281", admin.ListSongsHandler),
    ##########USER HANDLERS#################
    ("/register/google", user.UserAuthenticationHandler),
    ("/register/google/info", user.UserAuthenticationHandler)
]
