'''
Created on May 25, 2016

@author: kjm84
'''

import urllib2
import json
from pprint import pprint
from xml.dom import minidom

class ApolloRestConsumer(object):
    
    def __init__(self):
        print "Instantiated an ApolloRestConumer"

    def consumeJson(self, url):
        opener = urllib2.build_opener()
        jsonObj = json.loads(opener.open(url).read())
        pprint(jsonObj)
        return jsonObj

    def consumeXmlOther(self, urlPath):
        document = (urlPath, 'r')
        web = urllib2.urlopen(document)
        get_web = web.read()
        print get_web
        return get_web

    def parseDocumentXml(self, xmldoc):
        ontologyElements = xmldoc.getElementsByTagName('ontology')
        for ontologyElement in ontologyElements:
            nameData =  ontologyElement.getElementsByTagName('name')[0].firstChild.data
            print(nameData)

    def parseApolloXml(self, xmldoc):
#        caseCountElements = xmldoc.getElementsByTagName('data/item/epidemicCaseCounts/otherCaseCounts/Apollo_types_v3__1__0.CaseCount')
        dataElement = xmldoc.getElementsByTagName('data')[0]
        itemElement = dataElement.getElementsByTagName("item")[0]
        epidemicCaseCountsElement = itemElement.getElementsByTagName("epidemicCaseCounts")[0]
        otherCaseCountsElement = epidemicCaseCountsElement.getElementsByTagName("otherCaseCounts")[0]
        apolloTypesCaseCountsElements = otherCaseCountsElement.getElementsByTagName("Apollo_types_v3__1__0.CaseCount")
        for apolloTypesCaseCountElement in apolloTypesCaseCountsElements:
            countTitleElement = apolloTypesCaseCountElement.getElementsByTagName('countTitle')[0]
            nameData =  countTitleElement.firstChild.data
            print(nameData)
    
    def writeBrazilZikaOutputXml(self, localFileName, xmlAsString):
        self.writeXmlString("Brazil_Zika_Output.xml", xmlAsString)
    
    def writeChikungunyaOutputXml(self, localFileName, xmlAsString):
        self.writeXmlString("Chikungunya_Antigua_and_Barbuda_Output.xml", xmlAsString)
        
    def writeXmlString(self, localFileName, xmlAsString):
        text_file = open(localFileName, "w")
        text_file.write(xmlAsString)
        text_file.close()
    
    def consumeResponse(self, urlPath):
        usock = urllib2.urlopen(urlPath) 
        mResponse = usock.read()                  
        usock.close()                                              
        return mResponse

    def consumeXml(self, urlPath):
        usock = urllib2.urlopen(urlPath) 
        xmldoc = minidom.parse(usock)                              
        usock.close()                                              
        return xmldoc
    
    def readApolloXsd(self):
        xsdPath = "C:/ws/ws-python/apollo-xsd-and-types/src/main/resources/apollo_types_3.1.0.xsd"
        xsdFile = open(xsdPath, "r+")
        content = xsdFile.read();
        print "Read String is : ", content
        xsdFile.close()
        
def testJsonConsumption():
    apolloRestConsumer = ApolloRestConsumer()
    urlPath = "http://betaweb.rods.pitt.edu:80/apolloLibraryViewer-310-beta/api/v2/epidemic/8035"
    print(urlPath)
    epidemicJson = apolloRestConsumer.consumeJson(urlPath)
    pprint(epidemicJson) 
    urlPath = "http://betaweb.rods.pitt.edu:80/apolloLibraryViewer-310-beta/api/v2/epidemic/8035"
    print(urlPath)
    epidemicJson = apolloRestConsumer.consumeJson(urlPath)
    pprint(epidemicJson)
    
def editThenWriteResponse(responseString, urlPath):
    apolloRestConsumer = ApolloRestConsumer()
    print(responseString[2001:10000])
    xmlDoc = minidom.parseString(responseString)
    apolloRestConsumer.parseApolloXml(xmlDoc)
    xmlDoc = apolloRestConsumer.consumeXml(urlPath)
    apolloRestConsumer.parseDocumentXml(xmlDoc)
    print(xmlDoc.toxml)

#xmldoc = minidom.parse(usock)  
#xmldoc = consumeXml(urlPath)
#print xmldoc.toxml()       

def executeMain():
    epidemicIds = [ "8035", "8037", ]
    urlPath = "http://betaweb.rods.pitt.edu:80/apolloLibraryViewer-310-beta/api/v2/epidemic/8035?xml"
    urlPath = "http://data.bioontology.org/ontologies?apikey=24e1af42-54e0-11e0-9d7b-005056aa3316&format=xml"
    urlPath = "http://betaweb.rods.pitt.edu/apolloLibraryViewer-310-beta/api/v2/epidemic/8035.xml"
    urlPath = "http://betaweb.rods.pitt.edu/apolloLibraryViewer-310-beta/api/v2/epidemic/7961.xml"
    urlPath = "http://betaweb.rods.pitt.edu/apolloLibraryViewer-310-beta/7961.xml"
    print(urlPath) 
    apolloRestConsumer = ApolloRestConsumer()
    responseString = apolloRestConsumer.consumeResponse(urlPath)
    #responseString = responseString.replace("edu.pitt.apollo.types.", "Apollo_types_");
    apolloRestConsumer.writeChikungunyaOutputXml(responseString)
    #writeXmlString(responseString)
