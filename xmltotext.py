"""
Traverses the minidom tree and prints out the text nodes. (jfp:copied from the Web, then revised and added test data
still, the original function I copied is pretty bad; use toprettyxml() instead, as in the example below)
"""
from StringIO import StringIO
import xml.dom.minidom as domm
import sys
def xmltotxt(node, indentationLevel=0):
    print indentationLevel * ' ' + 'nodeName:' + node.nodeName
    #print node.firstChild.data
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            print child.data
        if child.nodeType == domm.Node.ELEMENT_NODE:
            xmltotxt(child, indentationLevel+4)

# test data...
import xml.dom.minidom
xml_ans="""<?xml version="1.0" encoding="UTF-8"?>
<esg:ESG xmlns:esg="http://www.earthsystemgrid.org/"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" 
         schemaLocation="http://vets.development.ucar.edu/schema/remoteMetadata.xsd">
        
        <esg:dataset name="ESM2M Model Output" state="published" source_catalog_uri="" id="cmip5.gfdl_esm2m">
                <esg:dataset name="ESM2M Control 1860 data" state="published" source_catalog_uri="" id="cmip5.gfdl_esm2m.ESM2M_Control-1860" />
        </esg:dataset>
        
</esg:ESG>
"""
dom = xml.dom.minidom.parseString(xml_ans)
xml_nws="""<?xml version="1.0" encoding="UTF-8"?><esg:ESG xmlns:esg="http://www.earthsystemgrid.org/" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" schemaLocation="http://vets.development.ucar.edu/schema/remoteMetadata.xsd"><esg:dataset name="ESM2M Model Output" state="published" source_catalog_uri="" id="cmip5.gfdl_esm2m" ><esg:dataset name="ESM2M Control 1860 data" state="published" source_catalog_uri="" id="cmip5.gfdl_esm2m.ESM2M_Control-1860" /></esg:dataset></esg:ESG>
"""
dnws = xml.dom.minidom.parseString(xml_nws)
# This works much better than the function xmltotxt, and basically echoes back xml_ans:
print dom.toprettyxml()


if __name__ == '__main__':
    # My XML was missing a doctype reference which the parser needs...
    dtd = '/home/hendry/inex/inex-1.4/dtd/xmlarticle.dtd'
    front = '\n\n' % dtd
    file = open(sys.argv[1])
    # ... and is added to the front of the article
    article = front + file.read()
    file.close()
    doc = domm.parse(StringIO(article))
    xmltotxt(doc.documentElement)


