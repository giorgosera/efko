import tornado.auth, tornado.web
from app.handlers.base import AjaxMessageException
from app.handlers import base
from app.model.video import *
from app.model.user import *

class UserAuthenticationHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("non-authenticated.html")
    
class UserLoginHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("login.html", msg_username="", msg_password="")
        
    def on_post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        msg_username = ""
        msg_password = ""
        
        user = User.objects(username=username)

        if len(user) > 0:
            user = user.get()
            success = user.correct_password(password)
        else:
            msg_username = "Username doesn't exist"
            success = False
             
        if success:
            self.clear_cookie("email")
            self.set_secure_cookie("email", user.email)
            self.redirect('/')
        else:
            msg_password = "Incorrect password"
            self.base_render("login.html", msg_username=msg_username, msg_password=msg_password)        
    
class UserRegistrationHandler(base.BaseHandler, tornado.auth.GoogleMixin):
    '''
    Authenticates user using OpenID
    '''
    @tornado.web.asynchronous
    def on_get(self):

        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
        
    def _on_auth(self, user):
        if not user:
            self.redirect('/')

        self.base_render("register.html", first=user['first_name'], last=user['last_name'], email=user['email'], msg="")
        
    def on_post(self):
        first_name = self.get_argument("first", None)
        last_name = self.get_argument("last", None)
        email = self.get_argument("email", None)
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        u = User()
        u.first_name = first_name
        u.last_name = last_name
        u.email = email
        u.create_password(password)
        ok = u.check_username(username)
        ok2 = u.check_email(u.email)
        if ok and ok2:
            u.username = username
            u.save()
            self.clear_cookie("email")
            self.set_secure_cookie("email", u.email)
            self.redirect('/')
        else:
            msg = "Username or email already registered"
            self.base_render("register.html", first=first_name, last=last_name, email=email, msg=msg)
            
        
class UserFBRegistrationHandler(base.BaseHandler, tornado.auth.FacebookGraphMixin):
    '''
    Handles the login for the Facebook user, returning a user object.
    '''
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
              redirect_uri='http://localhost:8888/register/facebook',
              client_id=self.settings["facebook_api_key"],
              client_secret=self.settings["facebook_secret"],
              code=self.get_argument("code"),
              callback=self.async_callback(
                self._on_login))
            return
        
        self.authorize_redirect(redirect_uri='http://localhost:8888/register/facebook',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream,offline_access"})
    
    def _on_login(self, user):
        u = FacebookUser.objects(email=user['link'])
        if len(u) == 0:
            new_u = FacebookUser()
            new_u.first_name = user['first_name']
            new_u.last_name = user['last_name']
            new_u.email = user['link'] #I use the url of the user profile as email
            new_u.username = new_u.first_name + new_u.last_name
            new_u.save()
            self.set_secure_cookie("email", new_u.email)
        else:
            u = u.get()
            self.set_secure_cookie("email", u.email)
        self.redirect("/")

class UserLogoutHandler(base.BaseHandler):
    '''
    Logout user.
    '''
    @tornado.web.authenticated
    def on_get(self):
        self.clear_cookie("email")
    
    def on_success(self):
        self.redirect('/')
        