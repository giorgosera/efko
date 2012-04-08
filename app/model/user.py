'''
Module app.model.user
------------------------

@author: George Eracleous
'''
import string, hashlib, random
from mongoengine import Document,StringField, EmbeddedDocument, ObjectIdField,  ListField#@UnresolvedImports 

class User(Document):
    meta = {"collection": "Users"}
    
    username = StringField(required=True, default="Anonnymous User")
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True, default="")
    salt = StringField(required=True, default="")
    covers_submitted = ListField(StringField(), default=list)
    voted_for = ListField(StringField(), default=list)
        
    def create_password(self, password):
        char_set = string.ascii_uppercase + string.digits 
        salt = ''.join(random.sample(char_set, 4))
        hash = hashlib.sha1(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        self.password = hash
        self.salt = salt
    
    def correct_password(self, given_pass):
        salt = self.salt
        return hashlib.sha1(salt.encode('utf-8') + given_pass.encode('utf-8')).hexdigest() == self.password
    
    def check_username(self, given_username):
        users = User.objects(username=given_username)
        if len(users) > 0:
            return False#username exists
        else:
            return True

    def check_email(self, given_email):
        users = User.objects(email=given_email)
        if len(users) > 0:
            return False#username exists
        else:
            return True
    
    def record_vote(self, sid):
        if sid not in self.voted_for:
            self.voted_for.append(sid)
            self.save()

    def record_submission(self, sid):
        if sid not in self.covers_submitted:
            self.covers_submitted.append(sid)
            self.save()
        
class CachedUser(EmbeddedDocument):
    name = StringField(required=True)
    id = ObjectIdField(required=True)
