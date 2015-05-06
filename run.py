#!/usr/bin/python

import os, sys, subprocess
dirname='Web_UI/'

from Web_UI import startupcheck, runserver

error = startupcheck()
if error == 0:
    runserver()
else:
    sys.exit()
