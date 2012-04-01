from app.handlers import base
from app.model.video import *

class ViewRankingsHandler(base.BaseHandler):
    '''
    Check user status and either load the home screen or the
    welcome page.
    '''
    def on_get(self):
        songs = [item for item in VideoItem.objects if not item.viewed]
        songs = sorted(songs, key=lambda song: -song.upvotes)        
        best = songs[:5]
        worst = songs[-5:]
        return best, worst
    
    def on_success(self, b, w):
        self.base_render("rankings.html", best=b, worst=w)
    