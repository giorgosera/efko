'''
Module app.model.video
------------------------

The models in this file are used to model
anything related to the video items:

@author: George Eracleous
'''

from mongoengine import Document, IntField, StringField, BooleanField#@UnresolvedImports 


class VideoItem(Document):
    meta = {"collection": "VideoItems"}

    url = StringField(required=True)
    title = StringField(required=True)
    artist = StringField(required=False)
    genre = StringField(required=False)
    uploader = StringField(required=True)
    upvotes = IntField(required=True, default=0)
    downvotes = IntField(required=True, default=0)
    viewed = BooleanField(required=True, default=False)