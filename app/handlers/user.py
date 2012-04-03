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
            self.base_render("submit.html")
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
            raise tornado.web.HTTPError(500, "Google auth failed")
        u = User()
        u.first_name = user['first_name']
        u.last_name = user['last_name']
        u.email = user['email'].lower()
        u.password = ""
        u.save(safe=True)
        self.base_render("register.html", uid=u.id)
        
    def on_post(self):
        uid = self.get_argument("uid", None)
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        u = User.objects(id=uid).get()
        u.create_password(password)
        u.username = username
        u.save()
        self.base_render("submit.html")

class UserLogoutHandler(base.BaseHandler):
    '''
    Logout user.
    '''
    @tornado.web.authenticated
    def on_get(self):
        self.clear_cookie("email")
    
    def on_success(self):
        self.redirect('/')
        