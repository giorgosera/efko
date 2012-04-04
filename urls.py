#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, home, admin, rankings, landing, user

url_patterns = [
    ("/", home.HomePageHandler),
    ("/next", home.HomePageHandler),
    ("/vote", home.VoteHandler),
    ("/rankings", rankings.ViewRankingsHandler),
    ("/submit", home.SubmitCoverHandler),
    ##########LANDING HANDLERS#################
    ("/terms", landing.TermsHandler),
    ("/privacy", landing.PrivacyHandler),
    ("/about", landing.AboutHandler),   
    ##########ARTISTS HANDLERS#################
    ("/voteforthis", home.UserPromotionHandler),
    ##########ADMIN HANDLERS#################
    ("/thisisasecreturl18211281", admin.ListSongsHandler),
    ##########USER HANDLERS#################
    ("/register", user.UserAuthenticationHandler),
    ("/login", user.UserLoginHandler),
    ("/logout", user.UserLogoutHandler),
    ("/login/info", user.UserLoginHandler),
    ("/register/google", user.UserRegistrationHandler),
    ("/register/google/info", user.UserRegistrationHandler)
]
