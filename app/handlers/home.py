from app.handlers import base
from app.model.video import *
from app.model.user import *
from random import shuffle
import tornado.web
import gdata.youtube#@UnresolvedImport
import gdata.youtube.service#@UnresolvedImport

yt_service = gdata.youtube.service.YouTubeService()

# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
yt_service.ssl = True
yt_service.developer_key = 'AI39si6XpFkJyW1UdXys9w9m6H_cpDomrAuo0UfM3kTH1WakeQBaTmyWuewZSeRkkPWR1iWj-xUDg2xBM0LefrmsIjk5Fbi-tw'
    
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
            
            similarity = 0.7*original_titles_jaccard + 0.3*titles_jaccard

            if similarity > 0.7:
                second_selection = song
                break
        
        if second_selection == None:
            second_selection = song
            
        first_selection.flagged_as_seen()
        second_selection.flagged_as_seen() 
          
        return first_selection, second_selection
    
    def on_success(self, f, s):
        self.base_render("intro.html", first=f, second=s, current_user_votes=[])
    
class VoteHandler(base.BaseHandler):
    
    @tornado.web.authenticated
    def on_post(self):
        sid = self.get_argument("sid", None)
        vi = VideoItem.objects(id=sid).get()
        current_user = self.get_current_user()
        current_user.record_vote(sid)
        vi.upvote()

class SubmitCoverHandler(base.BaseHandler):
    
    @tornado.web.authenticated
    def on_get(self):
        self.base_render("submit.html")

    @tornado.web.authenticated
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
                tags = unicode(video_entry.media.keywords.text, "utf-8")
                vi.tags = tags.split(', ')
                vi.artist = artist
                vi.genre = genre
                try:               
                    vi.save()
                except Exception, e:
                    print e
                user = self.get_current_user()
                user.record_submission(str(vi.id))

                msg = "The cover was submitted successfully."
                share_url = "youcover.me/voteforthis?cover="+str(vi.id)
            else:
                msg = "This cover already exists in the database."
        return (msg, share_url)
        
    def on_success(self, response, share_url):
        self.xhr_response.update({"msg": response, "share_url": share_url})  
        self.write(self.xhr_response)

class UserPromotionHandler(base.BaseHandler):
    '''
    Renders homepage with specific song
    '''
    def on_get(self, *args, **kwargs):
        sid = self.get_argument("cover")
        user = self.get_current_user()
        current_user_votes = []
        if user:
            current_user_votes = user.voted_for
        
        songs =  [item for item in VideoItem.objects if str(item.id) != sid]
        shuffle(songs)
        vi = VideoItem.objects(id=sid).get()
        first_selection = vi
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
            
            similarity = 0.7*original_titles_jaccard + 0.3*titles_jaccard

            if similarity > 0.7:
                second_selection = song
                break
        
        if second_selection == None:
            second_selection = song
            
        first_selection.flagged_as_seen()
        second_selection.flagged_as_seen() 
          
        return first_selection, second_selection, current_user_votes

    def on_success(self, f, s, cuv):
        self.base_render("intro.html", first=f, second=s, current_user_votes=cuv)   