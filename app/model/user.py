'''
Module app.model.user
------------------------

@author: George Eracleous
'''
import string, hashlib, random
from mongoengine import Document,StringField, EmbeddedDocument, ObjectIdField#@UnresolvedImports 

class User(Document):
    meta = {"collection": "Users"}
    
    username = StringField(required=True, default="Anonnymous User")
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True, default="")
    salt = StringField(required=True, default="")
    
    def create_password(self, password):
        char_set = string.ascii_uppercase + string.digits 
        salt = ''.join(random.sample(char_set, 4))
        hash = hashlib.sha1(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        self.password = hash
        self.salt = salt
    
    def correct_password(self, given_pass):
        salt = self.salt
        return hashlib.sha1(salt.encode('utf-8') + given_pass.encode('utf-8')).hexdigest() == self.password
        

class CachedUser(EmbeddedDocument):
    name = StringField(required=True)
    id = ObjectIdField(required=True)
