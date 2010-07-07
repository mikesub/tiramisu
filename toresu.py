#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
TODO:
1. решить с первичным копированием из src/dst
2. проверить добавления нового / удаление старого.
3. сделать modify_file рабочим.
4. разобраться с global
'''

import pyinotify, os, shutil
from xml.parsers import expat
from xml.dom import minidom

# here goes relative paths:
SRC = 'test/src'
DST = 'test/dst'

src = os.path.normpath(os.path.join(os.getcwd(), SRC))
dst = os.path.normpath(os.path.join(os.getcwd(), DST))

linenumbers = []
filename = ''

if os.path.exists(DST): shutil.rmtree(DST)
shutil.copytree(SRC,DST)

def update_file(source, remove=False):
    global filename
    relative = os.path.relpath(source, src)
    destination = os.path.join(dst,relative)
    
    if remove:
        os.remove(destination)
        print 'removed',destination
        return
    
    shutil.copy(source, destination)
    print source,'->',destination
    filename = relative
    #~ parse_file(path)

def parse_file(path):
    global linenumbers
    global filename
    def detect_template(name, attrs):
        if name == 'xsl:template':
            linenumbers.append(p.CurrentLineNumber)
    
    p = expat.ParserCreate()
    p.StartElementHandler = detect_template
    p.ParseFile(open(path,'r'))
    
    print filename, linenumbers
    modify_file(path)
    linenumbers = []
    filename = ''

def modify_file(path):
    contents = minidom.parse(path)
    templates = contents.getElementsByTagName('xsl:template')
    i = 0
    
    print filename
    for template in templates:
        if template.childNodes:
            print linenumbers[i],'(childnodes)'
        else:
            print linenumbers[i],'(empty)'
        i=+1
    
class ModifyHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        update_file(event.pathname)
    def process_IN_DELETE(self, event):
        update_file(event.pathname, True)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, ModifyHandler())
wm.add_watch(src, pyinotify.IN_MODIFY | pyinotify.IN_DELETE, rec=True, auto_add=True, exclude_filter=pyinotify.ExcludeFilter(['.*\.svn']))
notifier.loop()