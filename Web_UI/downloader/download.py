#!/usr/bin/python

import sys, os

if not os.path.isfile('config.json'):
    print('run "run.py" one time first, it will configure and check your dependencies')
    sys.exit()



import youtube_dl, json

#load configuration var
with open('config.json', 'r') as f:
         config = json.load(f)
f.close()

#pathtodownloader = config['pathtodownloader']
filein = config['filein']
fileout = config['fileout']
#debugenabled = config['debugenabled']
#listeningport = int(config['port'])
#hostname = config['host']


def filetostrings(filetoread):
    f = open(filetoread, 'r')
    string1 = []
    for line in f:
	string1.append(line)

    return string1


#set up youtube dl error handler
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#set up hook
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

#set up args for youtube-dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'ignoreerrors': True,
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#open file	
    f = open(fileout, "a")
#get link from the file
    todownloadlinks = filetostrings(filein)
#download and convert 
    for link in todownloadlinks:
	print(link)
	ydl.download([link])
	f.write(link+'\n')
	print('Done: '+link)

f.close()
print('Well Done')
sys.exit()

