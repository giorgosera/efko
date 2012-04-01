'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

from mongoengine import connect
from app.model.video import VideoItem
connect("efko_db")


    