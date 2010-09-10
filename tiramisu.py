#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyinotify, os, shutil, copy, sys, optparse
from lxml import etree 

NS = {
    'xsl':'http://www.w3.org/1999/XSL/Transform',
    'xhtml':'http://www.w3.org/1999/xhtml'
}

HTML = ['a','abbr','acronym','address','area','b','base','bdo','big','blockquote','body','br','button','caption','cite','code','col','colgroup','dd','del','dfn','div','dl','dt','em','fieldset','form','h1','head','hr','html','i','img','input','ins','kbd','label','legend','li','link','map','meta','noscript','object','ol','optgroup','option','p','param','pre','q','samp','script','select','small','span','strong','style','sub','sup','table','tbody','td','textarea','tfoot','th','thead','title','tr','tt','ul','var']
HTML_NS = ['//xhtml:'+i for i in HTML]
XPATH = ' | '.join(HTML_NS)

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
    relative = os.path.relpath(source, SRC)
    destination = os.path.join(DST,relative)
    
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
        elements = xml.xpath(XPATH,namespaces=NS)
        for element in elements:
            element.set('line',str(element.sourceline))
            element.set('file', str(str(filename).split('tiramisu/')[-1]) )
        xml.write(destination,xml_declaration=True,encoding='utf-8')
        print source,'->',filename
    except: pass
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
    SRC,
    pyinotify.IN_MODIFY | pyinotify.IN_DELETE,
    rec=True,
    auto_add=True
)
notifier.loop()