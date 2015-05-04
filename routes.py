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
import json
from flask import Flask, render_template, request, make_response, redirect, Markup

#load configuration var
with open('config.json', 'r') as f:
         config = json.load(f)
f.close()

pathtodownloader = config['pathtodownloader']
filein = config['filein']
fileout = config['fileout']
filein = pathtodownloader+filein
fileout = pathtodownloader+fileout
print(filein)
print(fileout)
debugenabled = config['debugenabled']
listeningport = int(config['port'])
hostname = config['host']

def showfile(filetoread):
    f = open(filetoread, 'r')
    string1 = ''
    for line in f:
	string1 = string1+'<li><a href="'+line+'" target="_blank" >'+line+'</a></li>'
    f.close()
    return string1


def addtofile(filein1, stringtoadd):
    f = open(filein1, 'a')
    s = stringtoadd+'\n'
    f.write(s)
    f.close()
    return 0

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app = Flask(__name__)

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
    shutdown_server()
    return 'Server shutting down...'
	    
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=debugenabled, port=listeningport, host=hostname)

sys.exit()
