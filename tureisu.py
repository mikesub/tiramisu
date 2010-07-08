#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyinotify, os, shutil, sys
from lxml import etree

NS = {'xsl':'http://www.w3.org/1999/XSL/Transform'}

# here goes relative paths:
SRC = 'test/src'
DST = 'test/dst'

src = os.path.normpath(os.path.join(os.getcwd(), SRC))
dst = os.path.normpath(os.path.join(os.getcwd(), DST))

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

    filename = os.path.join(DST,relative)
    parse_file(source)

def parse_file(path):
    global filename
    
    xml = etree.parse(path)
    templates = xml.xpath('/xsl:stylesheet/xsl:template',namespaces=NS)
    for template in templates:
        x = etree.SubElement(template,'template',attrib={
            'line':str(template.sourceline),
            'file':str(filename)
            })
        print etree.tostring(template)
        
    print source,'->',destination    
    filename = ''
    
class ModifyHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        update_file(event.pathname)
    def process_IN_DELETE(self, event):
        update_file(event.pathname, True)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, ModifyHandler())
wm.add_watch(src, pyinotify.IN_MODIFY | pyinotify.IN_DELETE, rec=True, auto_add=True, exclude_filter=pyinotify.ExcludeFilter(['.*\.svn']))
notifier.loop()
