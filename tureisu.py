#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyinotify, os, shutil, copy
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
    
def process_file(source, remove=False):
    global filename
    relative = os.path.relpath(source, src)
    destination = os.path.join(dst,relative)
    
    if remove:
        os.remove(destination)
        print 'removed',destination
        return

    filename = os.path.join(DST,relative)
    parse_file(source,destination)

def parse_file(source,destination):
    global filename
    
    try:
        xml = etree.parse(source)
        templates = xml.xpath('/xsl:stylesheet/xsl:template',namespaces=NS)
        for template in templates:
            attrs={
                'line':str(template.sourceline),
                'file':str(filename),
                'match':str(template.get('match'))
            }
            if template.get('mode'):
                attrs['mode'] =  str(template.get('mode'))
            if template.get('priority'):
                attrs['priority'] = str(template.get('priority'))

            el = etree.Element('template',attrib=attrs)

            for child in template:
                el.insert(0,child)
            
            if template.text:
                el.text = template.text
                template.text = ''
                
            template.insert(0,el)
         
        xml.write(destination,xml_declaration=True,encoding='utf-8')
    except:
        print source, 'failed to parse. just copied.'
        
    print source,'->',filename
    filename = ''

for root, dirs, files in os.walk(SRC):
    for file in files:
        process_file('/'.join([root, file]))
    
class ModifyHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        process_file(event.pathname, remove=False)
    def process_IN_DELETE(self, event):
        process_file(event.pathname, remove=True)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, ModifyHandler())
wm.add_watch(src, pyinotify.IN_MODIFY | pyinotify.IN_DELETE, rec=True, auto_add=True, exclude_filter=pyinotify.ExcludeFilter(['.*\.svn']))
notifier.loop()
