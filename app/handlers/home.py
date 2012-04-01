from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *
from random import shuffle

class WelcomePageHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("welcome.html")
    
class HomePageHandler(base.BaseHandler):
    '''
    Check user status and either load the home screen or the
    welcome page.
    '''
    def on_get(self):
        songs = [item for item in VideoItem.objects if not item.viewed]
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

class SubmitCoverHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("submit.html")
    
    def on_post(self):
        url = self.get_argument("url", None)
        title = self.get_argument("title", None)
        artist = self.get_argument("artist", None)
        genre = self.get_argument("genre", None)
        uploader = self.get_argument("uploader", None)
        response = True
        msg = ""        
        try:
            length = len(url)
            start = -1
            start = url.find('v=')
            if start >= 0:
                start += 2
                end = url[start:length].find('&')
                if end < 0:
                    end = length
                else:
                    end += start
                videoCode = url[start:end]
            else:
                videoCode = -1
                response = False
                msg = "Please input a valid Youtube url."
        except Exception, e:
            print e
        
        if response:
            vi = VideoItem()
            vi.url = 'http://www.youtube.com/v/' + videoCode + '?version=3&amp;hl=en_GB'
            vi.title = title
            vi.artist = artist
            vi.genre = genre
            vi.uploader = uploader
            #vi.save()
            msg = "The cover was submitted successfully."

        return (msg, )
        
    def on_success(self, response):
        self.xhr_response.update({"msg": response})  
        self.write(self.xhr_response)