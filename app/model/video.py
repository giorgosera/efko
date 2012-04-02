'''
Module app.model.video
------------------------

The models in this file are used to model
anything related to the video items:

@author: George Eracleous
'''

from mongoengine import Document, IntField, StringField, BooleanField, ListField#@UnresolvedImports 


class VideoItem(Document):
    meta = {"collection": "VideoItems"}

    url = StringField(required=True)
    title = StringField(required=True)
    artist = StringField(required=False)
    genre = StringField(required=False)
    uploader = StringField(required=True)
    upvotes = IntField(required=True, default=0)
    viewed = BooleanField(required=True, default=False)
    views = IntField(required=True, default=0)
    tags = ListField(StringField(), default=list)
    
    def upvote(self):
        '''
        It increases the votes of this song
        '''
        self.upvotes += 1
        self.save()
        
    def flagged_as_seen(self):
        '''
        If this videos has been seen by this user then we mark it
        as seen. The view ounter is also increased.
        '''
        #Uncomment when we have user objects
        #self.viewed = True
        self.views += 1
        self.save()
        