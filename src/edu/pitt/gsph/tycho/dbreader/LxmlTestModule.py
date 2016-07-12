'''
Created on Jun 10, 2016

@author: kjm84
'''

if __name__ == '__main__':
    pass

from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
from copy import deepcopy
from io import BytesIO
from DataSource import DataSource
from DataSource import ParserTarget
from lxml.builder import E
from lxml.builder import ElementMaker # lxml only !

def buildExampleTree():
    rootElement = etree.Element("root")
    rootElement.append( etree.Element("child1") )
    etree.SubElement(rootElement, "child2")
    etree.SubElement(rootElement, "child3")
    return rootElement

def prettyPrintTreeElement(rootElement):
    print(etree.tostring(rootElement, pretty_print=True))

def displayRootElementDiagnostics(rootElement):
    child = rootElement[0]
    print(child.tag)
    print(len(rootElement))
    print rootElement.index(rootElement[1]) # lxml.etree only!
    children = list(rootElement)
    print children
    for child in rootElement:
        print(child.tag)
        
def displaySlicingResults(rootElement):
    start = rootElement[:1]
    end   = rootElement[-1:]
    print(start[0].tag)
    print(end[0].tag)
    
def printChildren(rootElement):
    for child in rootElement:
        print(child.tag)
        
def moveLastToFirst(rootElement):
    if len(rootElement.length) > 1:
        rootElement[0] = rootElement[-1]  # this moves the element in lxml.etree! 
        
def simpleDiagnostics(rootElement):
    print "Is root an element? ", etree.iselement(rootElement)  # test if it's some kind of Element
    if len(rootElement): 
        isParent = rootElement is rootElement[0].getparent()  # lxml.etree only! test if it has children
        print "Does root element have children? ", isParent
    print "Childreen are"
    print([ c.tag for c in rootElement ])   

def pushElementToFront(rootElement, newElementTag):
    rootElement.insert(0, etree.Element(newElementTag))
    
def exampleMakingBranchCopyAdditions(branchToAdd):
    element = etree.Element("neu")
    element.append( deepcopy(branchToAdd) )
    prettyPrintTreeElement(element)
    
def examplePushToFront(rootElement, childTagName):
    pushElementToFront(rootElement, childTagName)
    simpleDiagnostics(rootElement)
    
def exampleAttrDictsOnElements():
    tychoRoot = etree.Element("Tycho", interesting="totally")
    print etree.tostring(tychoRoot)
    print(tychoRoot.get("interesting"))
    tychoRoot.set("hello", "Huhu")
    print tychoRoot.get("hello")
    print etree.tostring(tychoRoot)
    print sorted(tychoRoot.keys())
    for name, value in sorted(tychoRoot.items()):
        print('%s = %r' % (name, value))
        
def exampleAttrDictsUsingAttrib():
    tychoRoot = etree.Element("Tycho", interesting="totally")
    attributes = tychoRoot.attrib
    print(attributes["interesting"])
    print attributes.get("no-such-attribute")
    attributes["hello"] = "Guten Tag"
    print attributes["hello"]
    print tychoRoot.get("hello")
    d = dict(attributes)
    print sorted(d.items())
    
def exampleElementsContainingText():
    tychoRoot = etree.Element("root")
    tychoRoot.text = "TEXT"
    print(tychoRoot.text)
    print etree.tostring(tychoRoot)
    
def exampleDocumentStyleOrMixedStyle():
    htmlTree = etree.Element("html")
    body = etree.SubElement(htmlTree, "body")
    body.text = "TEXT"
    etree.tostring(htmlTree)
    br = etree.SubElement(body, "br")
    print etree.tostring(htmlTree)
    br.tail = "TAIL"
    print etree.tostring(htmlTree)
    return htmlTree

def exampleAddChildAndPrint():
    root = buildExampleTree()
    examplePushToFront(root, "child0")
    prettyPrintTreeElement(root)
    
def exampleXpath(rootTree):
    print(rootTree.xpath("string()"))
    build_text_list = etree.XPath("//text()")
    print(build_text_list(rootTree))
    texts = build_text_list(rootTree)
    print(texts[0])
    parent = texts[0].getparent()
    print(parent.tag)
    print(texts[1])
    print(texts[1].getparent().tag)
    print(texts[0].is_text)
    print(texts[1].is_text)
    print(texts[1].is_tail)
    stringify = etree.XPath("string()")
    print(stringify(rootTree))
    print(stringify(rootTree).getparent())
    
def exampleIteration():
    root = etree.Element("root")
    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "child").text = "Child 2"
    etree.SubElement(root, "another").text = "Child 3"
    prettyPrintTreeElement(root) 
    for element in root.iter():
        print("%s - %s" % (element.tag, element.text))
    for element in root.iter("child"):
        print("%s - %s" % (element.tag, element.text))
    for element in root.iter("another","child"):
        print("%s - %s" % (element.tag, element.text))
    return root

def exampleExtendedIteration():
    root = etree.Element("root")
    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "child").text = "Child 2"
    etree.SubElement(root, "another").text = "Child 3"
    root.append(etree.Entity("#234"))
    root.append(etree.Comment("some comment"))
    print("%s" % ("Trial One"))
    for element in root.iter():
        if isinstance(element.tag, basestring):
            print("%s - %s" % (element.tag, element.text))
        else:
            print("SPECIAL: %s - %s" % (element, element.text))
    print("%s" % "Trial Two")
    for element in root.iter(tag=etree.Element):
        print("%s - %s" % (element.tag, element.text))
    print("%s" % "Trial Three")
    for element in root.iter(tag=etree.Entity):
        print(element.text)
        
def exampleSerialization():
    root = etree.XML('<root><a><b/></a></root>')
    print etree.tostring(root)
    print(etree.tostring(root, xml_declaration=True))
    print(etree.tostring(root, encoding='iso-8859-1'))
    print(etree.tostring(root, pretty_print=True, encoding='iso-8859-1'))
    root = etree.XML('<html><head/><body><p>Hello<br/>World</p></body></html>')
    print etree.tostring(root) # default: method = 'xml'
    print etree.tostring(root, method='xml') # same as above
    print etree.tostring(root, method='html')
    print(etree.tostring(root, method='html', pretty_print=True))
    print etree.tostring(root, method='text')   
    br = next(root.iter('br'))  # get first result of iteration
    br.tail = u'W\xf6rld'
    #   print etree.tostring(root, method='text')  This blows up
    print etree.tostring(root, method='text', encoding="UTF-8")
    return root

def exampleElementTree():
    root = etree.XML('''<?xml version="1.0"?><!DOCTYPE root SYSTEM "test" [ <!ENTITY tasty "parsnips"> ]><root><a>&tasty;</a></root>''')
    tree = etree.ElementTree(root)
    print(tree.docinfo.xml_version)
    print(tree.docinfo.doctype)
    tree.docinfo.public_id = '-//W3C//DTD XHTML 1.0 Transitional//EN'
    tree.docinfo.system_url = 'file://local.dtd'
    print(tree.docinfo.doctype)
    print(etree.tostring(tree))
    print(etree.tostring(tree.getroot()))
    return root

def exampleFromString():
    some_xml_data = "<root>data</root>"
    root = etree.fromstring(some_xml_data)
    print(root.tag)
    print etree.tostring(root)
    return root

def exampleXmlFunction():
    root = etree.XML("<root>data</root>")
    print(root.tag)
    print etree.tostring(root)
    
def exampleParseFunction():
    some_file_like_object = BytesIO("<root>data</root>")
    tree = etree.parse(some_file_like_object)
    print etree.tostring(tree)
    root = tree.getroot()
    print(root.tag)
    print etree.tostring(root)
    return root

def openAndParseTychoXml():
    tychoXml = open("../Brazil_Zika_Output.xml", "r+")
    tychoTree = etree.parse(tychoXml)
    tychoRoot = tychoTree.getroot()
    print(tychoRoot.tag)
    for child in tychoRoot:
        print(child.tag)
    tychoXml.close()
    return tychoRoot

def parserObjectsExample():
    parser = etree.XMLParser(remove_blank_text=True) # lxml.etree only!
    root = etree.XML("<root>  <a/>   <b>  </b>     </root>", parser)
    print etree.tostring(root)
    for element in root.iter("*"):
        if element.text is not None and not element.text.strip():
            element.text = None
    print etree.tostring(root)
#    print help(etree.XMLParser) 
    return root

def exampleIncrementalParsing():
    dataSource = DataSource()
    tree = etree.parse(dataSource)
    print etree.tostring(tree)
    return tree.getroot()

def exampleIncrementalParsingTwo():
    parser = etree.XMLParser()
    parser.feed("<roo")
    parser.feed("t><")
    parser.feed("a/")
    parser.feed("><")
    parser.feed("/root>")
    root = parser.close()
    print etree.tostring(root)
    parser.feed("<root/>")
    root = parser.close()
    print etree.tostring(root)
    return root

def exampleIterativeParsing():
    some_file_like = BytesIO("<root><a>data</a></root>")
    for event, element in etree.iterparse(some_file_like):
        print("%s, %4s, %s" % (event, element.tag, element.text))
    some_file_like.close()
    some_file_like = BytesIO("<root><a>data</a></root>")
    for event, element in etree.iterparse(some_file_like, events=("start", "end")):                                  
        print("%s, %4s, %s" % (event, element.tag, element.text))
    some_file_like.close()
    some_file_like = BytesIO("<root><a>data</a></root>")
    tree = etree.parse(some_file_like)
    root = tree.getroot()
    return root

def exampleIterativeParsingTwo():
    some_file_like = BytesIO("<root><a><b>data</b></a><a><b/></a></root>")
    for _, element in etree.iterparse(some_file_like):
        if element.tag == 'b':
            print(element.text)
        elif element.tag == 'a':
            print("** cleaning up the subtree")
            element.clear()
    some_file_like.close()
    some_file_like = BytesIO("<root><a><b>data</b></a><a><b/></a></root>")
    tree = etree.parse(some_file_like)
    root = tree.getroot()
    return root

def exampleIterativeParsingThree():
    xml_file = BytesIO('''\
 <root>
   <a><b>ABC</b><c>abc</c></a>
   <a><b>MORE DATA</b><c>more data</c></a>
   <a><b>XYZ</b><c>xyz</c></a>
 </root>''')
    for _, element in etree.iterparse(xml_file, tag='a'):
        print('%s -- %s' % (element.findtext('b'), element[1].text))
        element.clear()
    xml_file.close()
    xml_file = BytesIO('''\
 <root>
   <a><b>ABC</b><c>abc</c></a>
   <a><b>MORE DATA</b><c>more data</c></a>
   <a><b>XYZ</b><c>xyz</c></a>
 </root>''')
    for _, element in etree.iterparse(xml_file, tag='a'):
        print('%s -- %s' % (element.findtext('b'), element.findtext('c')))
        element.clear()
    xml_file.close()
    
def exampleIterativeParsingFour():
    parser_target = ParserTarget()
    parser = etree.XMLParser(target=parser_target)
    events = etree.fromstring('<root test="true"/>', parser)
    print(parser_target.close_count)
    for event in events:
        print('event: %s - tag: %s' % (event[0], event[1]))
        for attr, value in event[2].items():
            print(' * %s = %s' % (attr, value))
    events = etree.fromstring('<root test="true"/>', parser)
    print(parser_target.close_count)
    events = etree.fromstring('<root test="true"/>', parser)
    print(parser_target.close_count)
    events = etree.fromstring('<root test="true"/>', parser)
    print(parser_target.close_count)

def exampleNamespacesOne():
    xhtml = etree.Element("{http://www.w3.org/1999/xhtml}html")
    body = etree.SubElement(xhtml, "{http://www.w3.org/1999/xhtml}body")
    body.text = "Hello World"
    print(etree.tostring(xhtml, pretty_print=True))


XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
XHTML = "{%s}" % XHTML_NAMESPACE
NSMAP = {None : XHTML_NAMESPACE} # the default namespace (no prefix)

def exampleNamespacesTwo():
    xhtml = etree.Element(XHTML + "html", nsmap=NSMAP) # lxml only!
    body = etree.SubElement(xhtml, XHTML + "body")
    body.text = "Hello World"
    print(etree.tostring(xhtml, pretty_print=True))
    print xhtml.nsmap
    
def exampleQname():
    tag = etree.QName('http://www.w3.org/1999/xhtml', 'html')
    print(tag.localname)
    print(tag.namespace)
    print(tag.text)
    tag = etree.QName('{http://www.w3.org/1999/xhtml}html')
    print(tag.localname)
    print(tag.namespace)
    root = etree.Element('{http://www.w3.org/1999/xhtml}html')
    tag = etree.QName(root)
    print(tag.localname)
    tag = etree.QName(root, 'script')
    print(tag.text)
    tag = etree.QName('{http://www.w3.org/1999/xhtml}html', 'script')
    print(tag.text)
    
def exampleNamespacesThree():
    root = etree.Element('root', nsmap={'a': 'http://a.b/c'})
    child = etree.SubElement(root, 'child',
                          nsmap={'b': 'http://b.c/d'})
    print len(root.nsmap)
    print len(child.nsmap)
    print child.nsmap['a']
    print child.nsmap['b']
    
def exampleNamespacesFour():
    xhtml = etree.Element(XHTML + "html", nsmap=NSMAP) # lxml only!
    body = etree.SubElement(xhtml, XHTML + "body")
    body.text = "Hello World"
    print(etree.tostring(xhtml, pretty_print=True))
    body.set(XHTML + "bgcolor", "#CCFFAA")
    print(etree.tostring(xhtml, pretty_print=True))
    print(body.get("bgcolor"))
    print body.get(XHTML + "bgcolor")
    find_xhtml_body = etree.ETXPath(      # lxml only !
        "//{%s}body" % XHTML_NAMESPACE)
    results = find_xhtml_body(xhtml)
    print(results[0].tag)
    for el in xhtml.iter('*'): print(el.tag)
    for el in xhtml.iter('{http://www.w3.org/1999/xhtml}*'): print(el.tag)
    for el in xhtml.iter('{*}body'): print(el.tag)
    print [ el.tag for el in xhtml.iter('{http://www.w3.org/1999/xhtml}body') ]
    print [ el.tag for el in xhtml.iter('body') ]
    print [ el.tag for el in xhtml.iter('{}body') ]
    print [ el.tag for el in xhtml.iter('{}*') ]




def CLASS(*args): # class is a reserved word in Python
    return {"class":' '.join(args)}

def exampleHtmlGeneration():
    page = (
       E.html(       # create an Element called "html"
       E.head(
         E.title("This is a sample document")),
       E.body(
         E.h1("Hello!", CLASS("title")),
         E.p("This is a paragraph with ", E.b("bold"), " text in it!"),
         E.p("This is another paragraph, with a", "\n      ",
         E.a("link", href="http://www.python.org"), "."),
         E.p("Here are some reservered characters: <spam&egg>."),
         etree.XML("<p>And finally an embedded XHTML fragment.</p>"))))
    print(etree.tostring(page, pretty_print=True))
    
    


def exampleXmlGeneration():
    E = ElementMaker(namespace="http://my.de/fault/namespace", nsmap={'p' : "http://my.de/fault/namespace"})
    DOC = E.doc
    TITLE = E.title
    SECTION = E.section
    PAR = E.par
    my_doc = DOC(
     TITLE("The dog and the hog"),
   SECTION(
     TITLE("The dog"),
     PAR("Once upon a time, ..."),
     PAR("And then ...")
   ),
   SECTION(
     TITLE("The hog"),
     PAR("Sooner or later ...")
   )
 )
    print(etree.tostring(my_doc, pretty_print=True))
    

def exampleEpath():
    root = etree.XML("<root><a x='123'>aText<b/><c/><b/></a></root>")
    print(root.find("b"))
    print(root.find("a").tag)
    print(root.find(".//b").tag)
    print [ b.tag for b in root.iterfind(".//b") ]
    print(root.findall(".//a[@x]")[0].tag)
    print(root.findall(".//a[@y]"))
    tree = etree.ElementTree(root)
    a = root[0]
    print(tree.getelementpath(a[0]))
    print(tree.getelementpath(a[1]))
    print(tree.getelementpath(a[2]))
    print tree.find(tree.getelementpath(a[2])) == a[2]
    print(root.find(".//b").tag)
    print(next(root.iterfind(".//b")).tag)
    print(next(root.iter("b")).tag)

exampleEpath()


def exampleXmlSchemaValidation():
    schema_root = etree.XML('''\
   <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
     <xsd:element name="a" type="xsd:decimal"/>
   </xsd:schema>''')
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema = schema)
    try:
        root = etree.fromstring("<a>5.3</a>", parser)
        prettyPrintTreeElement(root)
        print "validated xml against xschema"
    except:
        print "failed to validate"
        
exampleXmlSchemaValidation()
    
#exampleXmlGeneration()
#exampleNamespacesFour()
#exampleQname()
#exampleNamespacesTwo()

#exampleNamespacesOne()
#exampleNamespacesTwo()

#root = exampleIncrementalParsingTwo()
#root = openAndParseTychoXml()
#root = parserObjectsExample()
#root = exampleParseFunction()
#root = exampleXmlFunction()

#root = exampleFromString()
#exampleMakingBranchCopyAdditions(root[0])
#exampleAttrDictsOnElements()
#exampleAttrDictsUsingAttrib()
#exampleElementsContainingText()
#root = exampleDocumentStyleOrMixedStyle()
#exampleXpath(root)
#root = exampleExtendedIteration()
#root = exampleSerialization()
#root = exampleElementTree()

