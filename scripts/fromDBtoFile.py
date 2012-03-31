'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

from mongoengine import connect
from app.model.video import VideoItem
connect("efko_db")

while (True):
    title = raw_input("Song's title")
    artist = raw_input("Who's the artist?")
    uploader = raw_input("Who's the uploader?")
    genre = raw_input("What's the genre?")
    
    vi = VideoItem()
    vi.title = tile
    vi.artist = artist
    vi.uploader = uploader
    vi.genre = genre
    vi.save()
    