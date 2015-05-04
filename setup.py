#!/usr/bin/python

import sys, os, json


config = {
	'host' : '0.0.0.0',
	'port' : 1234,
	'pathtodownloader' : 'downloader/',
	'filein' : 'todownload',
	'fileout' : 'downloaded',
	'debugenabled' : 'True',
	}
f = open(config['pathtodownloader']+config['filein'], 'w')
f.close()
f = open(config['pathtodownloader']+config['fileout'], 'w')
f.close()

with open('config.json', 'w') as f:
    json.dump(config, f)

f.close()
with open(config['pathtodownloader']+'config.json', 'w') as f:
    json.dump(config, f)

f.close()
