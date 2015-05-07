#!/usr/bin/python

import os, sys



dirname='Web_UI/'

from Web_UI import startupcheck, runserver, rundownloader 

error = startupcheck()
#if no error in checking run server
if error == 0:

#choose arg to handle
    if 2==len(sys.argv):
	if sys.argv[1]=='-d':
	    print('enter in download only mode')
	    rundownloader()
	    sys.exit()
    else:
	runserver()


else:
    sys.exit()
