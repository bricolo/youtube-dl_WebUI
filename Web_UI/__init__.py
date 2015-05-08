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

import os
import sys
stop = 0

def startupcheck():
    if os.path.isfile('Web_UI/FIRSTRUN'):
	error=0
	print('Assuming you have os and sys imported')
	print('Try to import json')
#check if you have json installed
	try:
	    import json
	except ImportError:
	    error = 1
	    print("json is not installed in python")
#create config file
	if not error==1:
	    print('creating file and config...')
	    config = {
		'host' : '0.0.0.0',
		'port' : 1234,
		'pathtodownloader' : 'downloader/',
		'appdir' : 'Web_UI/',
		'filein' : 'todownload',
		'fileout' : 'downloaded',
		'debugenabled' : 'True',
		'firstrunfile' : 'FIRSTRUN',
		}
	    f = open(config['appdir']+config['pathtodownloader']+config['filein'], 'w')
	    f.close()
	    f = open(config['appdir']+config['pathtodownloader']+config['fileout'], 'w')
	    f.close()
	    with open(config['appdir']+'config.json', 'w') as f:
		json.dump(config, f)
	    f.close()
	    #with open(config['appdir']+config['pathtodownloader']+'config.json', 'w') as f:
		#json.dump(config, f)
	    #f.close()
#check if you have flask installed
	print('Try to import flask...')
	try:
	    import flask
	except ImportError:
	    error = 1
	    print("Flask is not installed in python")
#check if you have youtube_dl python library installed
	print('Try to import youtube_dl')
	try:
	    import youtube_dl
	except ImportError:
	    error = 1
	    print("Youtube-dl is not installed in python")
	#return 0 if all OK    
	try:
	    import subprocess
	except ImportError:
	    error = 1
	    print("subprocess is not installed in python")
	try:
	    import multiprocessing
	except ImportError:
	    error = 1
	    print("multiprocessing is not installed in python")
	if error == 1:
	    print("Some errors cannot start, try 'pip install ' to install dependencies")
	    return 1
	else:
	    os.remove(config['appdir']+config['firstrunfile'])
	    print("All mightwork;) starting...")
	    return 0
    else:
	return 0
#end


def rundownloader():
   from subprocess import call
   import json
   with open('Web_UI/config.json', 'r') as f:
       config = json.load(f)
   f.close()
   appdir = config['appdir']
   pathtodownloader = config['pathtodownloader']
   pathtodownloader = appdir+pathtodownloader
   call(pathtodownloader+'download.py')
   return 0
#end

def whiledownloader():
    global stop
    import time
    print("testlol")    
    while stop == 0:
	time.sleep(20)
	rundownloader()


def runserver():

#ensure that you run setup first
    if os.path.exists('Web_UI/FIRSTRUN'):
	print('run setup.py first')
	exit.exit()

#import 
    import time
    import json
    from flask import Flask, render_template, request, make_response, redirect, Markup
    import threading
    global stop
    download_thread = threading.Thread(target=whiledownloader)

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
    debugenabled = config['debugenabled']
    listeningport = int(config['port'])
    hostname = config['host']
    filelock = pathtodownloader+'LOCK'
#declare function
    def showfile(filetoread):
	f = open(filetoread, 'r')
	string1 = ''
	for line in f:
	    string1 = string1+'<li><a href="'+line+'" target="_blank" >'+line+'</a></li>'
	f.close()
	return string1


    def addtofile(filein1, stringtoadd):
	lockfile(filelock, 1)
	f = open(filein1, 'a')
	s = stringtoadd+'\n'
	f.write(s)
	f.close()
	lockfile(filelock, 0)
	return 0

    def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
	    raise RuntimeError('Not running with the Werkzeug Server')
	func()

    def lockfile(filelocker, lock):
	if lock==1:
	    while os.path.isfile(filelocker):
		time.sleep(5)
	    open(filelocker, 'a').close()
	else:
	    os.remove(filelocker)
	return 0


#create a new flask in app
    app = Flask(__name__)
#routing rules
    @app.route('/')
    def home():
	return render_template('home.html', todownload=Markup(showfile(filein)), downloaded=Markup(showfile(fileout)))

    @app.route("/add1", methods=['POST'])
    def add1():
	linktoadd = request.form['link']
	addtofile(filein, linktoadd)
	app.logger.debug(linktoadd)
	return render_template('add1.html', link=linktoadd)
    @app.route("/shutdown")
    def shutdown():
	stop = 1
	shutdown_server()
	return 'Server shutting down...'
		
    @app.errorhandler(404)
    def not_found(error):
	return render_template('error.html'), 404
    
    #start
    app.run(debug=debugenabled, port=listeningport, host=hostname)
#exit when server stop
    sys.exit()


