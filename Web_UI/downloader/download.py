#!/usr/bin/python
# -*- coding: utf8 -*-

#/************************************************************************************
# * *************************************************************************************
# * **    This file is a part of youtube-dl_WebUI a simple full python web ui for youtube-dl
# * **    Contact: bricolo.code@gmail.com
# * **
# * *************************************************************************************
# * *************************************************************************************
# * **
# * **    Copyright (C) 2015 bricolo
# * **    This program is free software: you can redistribute it and/or modify
# * **    it under the terms of the GNU General Public License as published by
# * **    the Free Software Foundation, either version 3 of the License, or
# * **    (at your option) any later version.
# * **
# * **    This program is distributed in the hope that it will be useful,
# * **    but WITHOUT ANY WARRANTY; without even the implied warranty of
# * **    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * **    GNU General Public License for more details.
# * **
# * **    You should have received a copy of the GNU General Public License
# * **    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# * **
# * ***********************************************************************************/

import sys, os

if not os.path.isfile('Web_UI/config.json'):
    print('run "run.py" one time first, it will configure and check your dependencies')
    sys.exit()



import youtube_dl, json
#load configuration var
with open('Web_UI/config.json', 'r') as f:
         config = json.load(f)
f.close()
appdir = config['appdir']
pathtodownloader = config['pathtodownloader']
pathtodownloader = appdir+pathtodownloader
filein = config['filein']
fileout = config['fileout']
filein = pathtodownloader+filein
fileout = pathtodownloader+fileout
filelock = pathtodownloader+'LOCK'
#debugenabled = config['debugenabled']
#listeningport = int(config['port'])
#hostname = config['host']
def lockfile(filelocker, lock):
    if lock==1:
	while os.path.isfile(filelocker):
	    time.sleep(5)
	open(filelocker, 'a').close()
    else:
	os.remove(filelocker)
    return 0

def preprocessing(filetoprocess):
# Get file contents
    fd = open(filetoprocess)
    contents = fd.readlines()
    fd.close()
    new_contents = []
# Get rid of empty lines
    for line in contents:
	# Strip whitespace, should leave nothing if empty line was just "\n"
	if not line.strip():
	    continue
	# We got something, save it
	else:
	    new_contents.append(line)
    return new_contents

if len(preprocessing(filein))>0:

    def filetostrings(filetoread):
	f = open(filetoread, 'r')
	string1 = []
	for line in f:
	    if not line.strip():
		continue
	    else:
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
	    f = open(pathtodownloader+'download.log', 'a')
	    f.write(msg)
	    f.close

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
#get link from the file
	todownloadlinks = filetostrings(filein)
#download and convert 
	for link in todownloadlinks:
	    print(link)
	    ydl.download([link])
	    print('Done: '+link)
#write downloaded link to file out
	lockfile(filelock, 1)
	with open(fileout,"a") as output: 
	    for line in todownloadlinks:
		    output.write(line)
	    f.close()
#erase downloaded link from file in 
	todownloadnext =  filetostrings(filein)
	open(filein, 'w').close()#erase file in
	for line in todownloadnext:#remove downloaded link from the list
	    if line in todownloadlinks:
		todownloadnext.remove(link)
	with open(filein,"a") as output:#write non downloaded link
	    for line in todownloadnext:
		output.write(line)
	lockfile(filelock, 0)
else:#if nothing in todownload
    print('Nothing to download')

print('Well Done')


