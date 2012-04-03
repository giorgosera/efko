'''
Module app.model.user
------------------------

@author: George Eracleous
'''
import string, hashlib, random
from mongoengine import Document,StringField#@UnresolvedImports 

class User(Document):
    meta = {"collection": "Users"}
    
    username = StringField(required=True, default="Anonnymous User")
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True, default="")
    
    def create_password(self, password):
        char_set = string.ascii_uppercase + string.digits 
        salt = ''.join(random.sample(char_set, 4))
        hash = hashlib.sha1(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        self.password = hash
        self.salt = salt
        