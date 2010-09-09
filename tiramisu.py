#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyinotify, os, shutil, copy, sys, optparse
from lxml import etree 

NS = {
    'xsl':'http://www.w3.org/1999/XSL/Transform',
    'xhtml':'http://www.w3.org/1999/xhtml'
}

parser = optparse.OptionParser()
parser.add_option('-d','--dir', dest='dir', help='path to XHH directory')
(options, args) = parser.parse_args()

if options.dir is None:
    parser.print_help()
    sys.exit()

SRC = os.path.normpath(os.path.join(os.getcwd(), options.dir, 'xsl'))
DST = os.path.normpath(os.path.join(SRC, '../tiramisu'))

filename = ''

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC,DST)
    
def process_file(source, remove=False):
    global filename
    relative = os.path.relpath(source, src)
    destination = os.path.join(dst,relative)
    
    if remove:
        os.remove(destination)
        print 'removed',destination
        return

    filename = os.path.normpath(os.path.join(DST,relative))
    parse_file(source,destination)

def parse_file(source,destination):
    global filename
    
    try:
        xml = etree.parse(source)
        elements = xml.xpath('//div',namespaces=NS)
        for element in elements:
            element.set('line',str(element.sourceline))
            element.set('file', str(str(filename).split('xsl/')[1]) )
        xml.write(destination,xml_declaration=True,encoding='utf-8')
        print source,'->',filename
    except:
        print source,' not parsed.'
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

wm.add_watch(
    src,
    pyinotify.IN_MODIFY | pyinotify.IN_DELETE,
    rec=True,
    auto_add=True
)
notifier.loop()