from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *
from random import shuffle

class HomePageHandler(base.BaseHandler):
    '''
    Check user status and either load the home screen or the
    welcome page.
    '''
    def on_get(self):
        songs = [item for item in VideoItem.objects]
        shuffle(songs)
        first_selection = songs.pop(0)
        for song in songs:
            if first_selection.title == song.title:
                second_selection = song
                break
        first_selection.flagged_as_seen()
        second_selection.flagged_as_seen() 
          
        return first_selection, second_selection
    
    def on_success(self, f, s):
        self.base_render("intro.html", first=f, second=s)
    
class VoteHandler(base.BaseHandler):

    def on_post(self):
        sid = self.get_argument("sid", None)
        vi = VideoItem.objects(id=sid).get()
        vi.upvote()
        
        
    