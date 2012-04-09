'''
Created on 13 Nov 2011

@author: george

This module accesses a .db file and reads the entries and then write them to a file.
'''

from app.model.video import *

for video in VideoItem.objects():
    url = video.url
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
        
    video.url = 'http://www.youtube.com/v/' + videoCode + '?wmode=opaque?version=3&amp;hl=en_GB'
    video.save()

    