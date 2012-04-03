from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *
from random import shuffle

import gdata.youtube#@UnresolvedImport
import gdata.youtube.service#@UnresolvedImport

yt_service = gdata.youtube.service.YouTubeService()

# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
yt_service.ssl = True
yt_service.developer_key = 'AI39si6XpFkJyW1UdXys9w9m6H_cpDomrAuo0UfM3kTH1WakeQBaTmyWuewZSeRkkPWR1iWj-xUDg2xBM0LefrmsIjk5Fbi-tw'


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
        second_selection = None
        tags_first = set(first_selection.tags)
        title_first = set(first_selection.title)
        original_title_first = set(first_selection.original_title) 
        for song in songs:
            
            #Code to compute similarity
            title_song = set(song.title)
            titles_intersection = title_song & title_first
            titles_union =  title_song | title_first
            titles_jaccard = float(len(titles_intersection))/float(len(titles_union))
            
            original_title_song = set(song.original_title)
            original_titles_intersection = original_title_song & original_title_first
            original_titles_union =  original_title_song | original_title_first
            original_titles_jaccard = float(len(original_titles_intersection))/float(len(original_titles_union))
            
            similarity = 0.5*original_titles_jaccard + 0.5*titles_jaccard

            if similarity > 1.7:
                second_selection = song
                break
        
        if second_selection == None:
            second_selection = song
            
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
            video_entry = yt_service.GetYouTubeVideoEntry(video_id=videoCode)
            vi = VideoItem()
            vi.url = 'http://www.youtube.com/v/' + videoCode + '?version=3&amp;hl=en_GB'
            if not len(VideoItem.objects(url = vi.url)) > 0:
                vi.title = video_entry.media.title.text
                vi.original_title = title
                vi.uploader = video_entry.author[0].name.text
                user_entry = yt_service.GetYouTubeUserEntry(username=vi.uploader)
                vi.uploader_url = user_entry.link[0].href
                tags = video_entry.media.keywords.text
                vi.tags = tags.split(', ')
                vi.artist = artist
                vi.genre = genre            
                vi.save()
                msg = "The cover was submitted successfully."
            else:
                msg = "This cover already exists in the database."
        return (msg, )
        
    def on_success(self, response):
        self.xhr_response.update({"msg": response})  
        self.write(self.xhr_response)

        