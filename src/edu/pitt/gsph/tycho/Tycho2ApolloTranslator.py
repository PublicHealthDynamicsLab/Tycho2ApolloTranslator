'''
Created on Jun 28, 2016

@author: kjm84
'''

import MySQLdb
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
from Tycho2ApolloCaseCountSpecifier import CaseCountSpecifier
from ApolloRestConsumer import ApolloRestConsumer
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import sys

if __name__ == '__main__':
    pass

def generateXmlQueryResponse():
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    elementEpidemic = buildQualifiedElement("Epidemic")
    buildEpidemic(elementEpidemic)
    tychoXml = etree.tostring(elementEpidemic, pretty_print=True)
    xml_validator(tychoXml,"./apollo_types_3.1.0.xsd")
    writeResultXml(tychoXml)

def trialValidation():
    tychoXml = open("a.xml", "r").read()
    xml_validator(tychoXml,"./a.xsd")

def writeResultXml(tychoXml):
    fo = open("t.xml", "wb")
    fo.write(tychoXml)
    fo.close()

def xml_validator(some_xml_string, xsd_file='/path/to/my_schema_file.xsd'):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
        print "YEAH!, my xml file has validated"
    except XMLSyntaxError as e:
        #handle exception here
        print "Oh NO!, my xml file does not validate"
        print e
        pass
  
def buildResponseWrapper():
    elementResourceResponse = etree.Element("edu.pitt.isg.types.rest.ResourceResponse")
    elementMeta = buildElementMeta()
    elementData = etree.Element("data")
    etree.SubElement(elementData, "name").text = "2013, Antigua and Barbuda"
    elementItem = etree.SubElement(elementData, "item")
    elementResourceResponse.append(elementMeta)
    elementResourceResponse.append(elementData)
    buildEpidemic(elementItem)
    return elementResourceResponse
    
def buildEpidemic(elementItem):
    elementCausalPathogens = buildQualifiedElement("causalPathogens")
    elementItem.append(elementCausalPathogens)
    elementEpidemicPeriod = buildQualifiedElement("epidemicPeriod")
    elementAdministrativeLocations = buildQualifiedElement("administrativeLocations")
    elementInfections = buildQualifiedElement("infections")
    elementEpidemicCaseCounts = buildQualifiedElement("epidemicCaseCounts")
    elementReferences = buildQualifiedElement("references")
    elementEditHistory = buildQualifiedElement("editHistory")
    elementEpidemic = elementItem
    populateAppendCausalPathogens(elementEpidemic, elementCausalPathogens)
    populateAppendEpidemicPeriod(elementEpidemic, elementEpidemicPeriod)
    populateAppendAdministrativeLocations(elementEpidemic, elementAdministrativeLocations)
    populateAppendInfections(elementEpidemic, elementInfections)
    populateAppendEpidemicCaseCounts(elementEpidemic, elementEpidemicCaseCounts)
    populateAppendReferences(elementEpidemic, elementReferences)
    populateAppendEditHistory(elementEpidemic, elementEditHistory)
    return elementEpidemic

def buildElementMeta():
    elementMeta = etree.Element("meta")
    elementStatus = etree.Element("status")
    elementStatusMessage = etree.Element("statusMessage")
    elementSource = etree.Element("source")
    elementNumberOfReturnedResults = etree.Element("numberOfReturnedResults")
    elementStatus.text = "200"
    elementStatusMessage.text = "OK"
    elementSource.text = "Powered by the Apollo Library v3.1.0"
    elementNumberOfReturnedResults.text = "1"
    elementMeta.append(elementStatus)
    elementMeta.append(elementStatusMessage)
    elementMeta.append(elementSource)
    elementMeta.append(elementNumberOfReturnedResults)
    return elementMeta

def populateAppendCausalPathogens(elementEpidemic, elementCausalPathogens):
    tag = etree.QName('http://types.apollo.pitt.edu/v3_1_0/', 'ncbiTaxonId')
    elementNcbiTaxonId = etree.Element(tag)
    elementNcbiTaxonId.text = "37124"
    elementCausalPathogens.append(elementNcbiTaxonId)
    elementEpidemic.append(elementCausalPathogens)
    
def buildQualifiedElement(elementName):
    tag = etree.QName('http://types.apollo.pitt.edu/v3_1_0/', elementName)
    return etree.Element(tag)
    
def buildDate(elementName,year,month,day,timezone,hour,minute,second):
    elementDate = buildQualifiedElement(elementName)
#    2000-01-12T12:13:14Z
    formattedDate = year + "-" + month.zfill(2) + "-" + day.zfill(2) 
#    formattedDate = formattedDate + "T" + hour.zfill(2) + ":" + minute.zfill(2)  + ":" + second.zfill(2)  + "Z"
    print formattedDate
    elementDate.text = formattedDate
#    etree.SubElement(elementDate, "year").text = year
#    etree.SubElement(elementDate, "month").text = month
#    etree.SubElement(elementDate, "day").text = day
#    etree.SubElement(elementDate, "timezone").text = timezone
#    etree.SubElement(elementDate, "hour").text = hour
#    etree.SubElement(elementDate, "minute").text = minute
#    etree.SubElement(elementDate, "second").text = second
    return elementDate
    
def populateAppendEpidemicPeriod(elementEpidemic, elementEpidemicPeriod):
    elementStartDate = buildDate("startDate","2014","1","4","0","0","0","0")
    elementStartDateDefinition = buildQualifiedElement("startDateDefinition")
    elementStartDateDefinition.text = "symptomOnsetFirstCase"
    elementEndDateDefinition = buildQualifiedElement("endDateDefinition")
    elementEndDateDefinition.text = "symptomOnsetLastCase"
    elementEpidemicPeriod.append(elementStartDate)
    elementEpidemicPeriod.append(elementStartDateDefinition)
    elementEpidemicPeriod.append(elementEndDateDefinition)      
    elementEpidemic.append(elementEpidemicPeriod)
    
def populateAppendAdministrativeLocations(elementEpidemic, elementAdministrativeLocations):
#    etree.SubElement(elementAdministrativeLocations, "string").text = "5097"
    elementAdministrativeLocations.text = "5097"
    elementEpidemic.append(elementAdministrativeLocations)
    
def populateAppendEpidemicZones(elementEpidemic, elementEpidemicZones):
    elementEpidemic.append(elementEpidemicZones)

def buildCausalPathogen(ncbiTaxonId):
    elementCausalPathogen = etree.Element("causalPathogen")
    elementNcbiTaxonId = etree.Element("ncbiTaxonId")
    elementNcbiTaxonId.text = ncbiTaxonId
    elementCausalPathogen.append(elementNcbiTaxonId)
    return elementCausalPathogen

def populateAppendInfections(elementEpidemic, elementInfections):
#    elementInfection = etree.Element("edu.pitt.apollo.types.v3__1__0.Infection")
    elementPathogen = buildQualifiedElement("pathogen")
    elementInfections.append(elementPathogen)
    elementNcbiTaxonId = buildQualifiedElement("ncbiTaxonId")
    elementNcbiTaxonId.text = "9606"
    elementPathogen.append(elementNcbiTaxonId)
#    elementInfectionPathogen = etree.SubElement(elementInfection, "pathogen")
#    elementInfectionPathogen
    elementHost = buildQualifiedElement("host")
    elementHost.text = "9606"
    elementInfections.append(elementHost)
#    etree.SubElement(elementInfection, "host").text = "9606"
#    elementInfectiousDiseases = etree.Element("infectiousDiseases")
#    elementInfectiousDisease = etree.Element("edu.pitt.apollo.types.v3__1__0.InfectiousDisease")
#    etree.SubElement(elementInfectiousDisease, "disease").text = "111864006"
#    etree.SubElement(elementInfectiousDisease, "speciesWithDisease").text = "9606"
#    elementCausalPathogen = buildCausalPathogen("37124")
#    elementInfectiousDisease.append(elementCausalPathogen)
#    elementInfectiousDiseases.append(elementInfectiousDisease)
#    elementInfection.append(elementInfectiousDiseases)
#    etree.SubElement(elementInfection, "infectionAcquisitionsFromInfectedHosts")
#    elementInfections.append(elementInfection)
    elementEpidemic.append(elementInfections)    
    
def populateAppendPopulationSerologySurveys(elementEpidemic, elementPopulationSerologySurveys):
    elementEpidemic.append(elementPopulationSerologySurveys)    
    
def populateAppendPopulationInfectionSurveys(elementEpidemic, elementPopulationInfectionSurveys):
    elementEpidemic.append(elementPopulationInfectionSurveys)    
    
def populateAppendInfectiousDiseaseControlStrategies(elementEpidemic, elementInfectiousDiseaseControlStrategies):
    elementEpidemic.append(elementInfectiousDiseaseControlStrategies)    
    
def populateAppendCaseDefinitions(elementEpidemic, elementCaseDefinitions):
    elementEpidemic.append(elementCaseDefinitions)        
    
def populateAppendContactDefinitions(elementEpidemic, elementContactDefinitions):
    elementEpidemic.append(elementContactDefinitions)
        
def queryWeeklyReportedCounts(locationId, diseaseSubCategoryId): 
    dbUsername = sys.argv[1]
    dbPassword = sys.argv[2]  
    db = MySQLdb.connect("localhost", dbUsername, dbPassword, "tycho_dev_v2", 3308 )
    cursor = db.cursor()
    sql = "select year, week, number from weekly_reported_counts where location_id = %s and dis_sub_id = %s order by year, week" % (locationId, diseaseSubCategoryId)
    cursor.execute(sql)
    results = cursor.fetchall()
    cummulativeCaseNumber = 0
    caseCountSpecifier = CaseCountSpecifier()
    caseCountSpecifier.title = "Cumulative diphtheria cases updated weekly since 1895"
    caseCountSpecifier.definitions.append("CASES")
    caseCountSpecifier.definitions.append("DEATHS")
    caseCountSpecifier.arrayType = 'cumulativeWithoutResets'
    caseCountSpecifier.firstArrayAxis = 'timeSpan'
    isFirst = True
    for row in results:
        yearNumber = row[0]
        weekNumber = row[1]
        caseNumber = int(row[2]) 
        cummulativeCaseNumber = cummulativeCaseNumber + caseNumber  
        if (isFirst):
            firstWeekOffset = weekNumber - 1             
            firstDay = datetime(yearNumber,1,1) + relativedelta(weeks=+firstWeekOffset)
            isFirst = False              
        lastDay = datetime(yearNumber,1,1) + relativedelta(weeks=+weekNumber)
        lastDay = lastDay + relativedelta(days=+7)
        caseCountSpecifier.firstYears.append(str(firstDay.year))
        caseCountSpecifier.firstMonths.append(str(firstDay.month))
        caseCountSpecifier.firstDays.append(str(firstDay.day))
        caseCountSpecifier.lastYears.append(str(lastDay.year))
        caseCountSpecifier.lastMonths.append(str(lastDay.month))
        caseCountSpecifier.lastDays.append(str(lastDay.day))
        caseCountSpecifier.counts.append(str(cummulativeCaseNumber))
    db.close()
    return caseCountSpecifier

def populateAppendEpidemicCaseCounts(elementEpidemic, elementEpidemicCaseCounts):
    elementOtherCaseCounts = buildQualifiedElement("otherCaseCounts")
    caseCountSpecifiers = []
    caseCountSpecifiers.append(queryWeeklyReportedCounts(3313, 14))
    for caseCountSpecifier in caseCountSpecifiers:
        buildCaseCount(elementOtherCaseCounts, caseCountSpecifier)
    elementEpidemicCaseCounts.append(elementOtherCaseCounts)
    elementEpidemic.append(elementEpidemicCaseCounts)  

def populateAppendCaseLists(elementEpidemic, elementCaseLists):
    elementEpidemic.append(elementCaseLists)

def buildCaseCount(elementCaseCount, spec):
    elementCountTitle = buildQualifiedElement("countTitle")
    elementCountTitle.text = spec.title
    elementCaseDefinitionsIncluded = buildQualifiedElement("caseDefinitionsIncluded")
    elementCaseDefinitionsIncluded.text = "confirmedCase"
    elementCaseCount.append(elementCountTitle)
    elementCaseCount.append(elementCaseDefinitionsIncluded)
    elementCaseCountArrayDescription = buildQualifiedElement("caseCountArrayDescription")
    elementCaseCountArrayType = buildQualifiedElement("caseCountArrayType")
    elementCaseCountArrayType.text = spec.arrayType
    elementCaseCountArrayDescription.append(elementCaseCountArrayType)
    elementCaseCount.append(elementCaseCountArrayDescription)
    elementCaseCountArray = buildQualifiedElement("caseCountArray")
    elementFirstArrayAxis = buildQualifiedElement("firstArrayAxis")
    elementCaseCountArray.append(elementFirstArrayAxis)
    elementName = buildQualifiedElement("name")
    elementName.text = spec.firstArrayAxis
    elementFirstArrayAxis.append(elementName)
    for idx in range(len(spec.lastYears)):
        elementFirstDay = buildDate("firstDay", spec.firstYears[idx], spec.firstMonths[idx], spec.firstDays[idx], "0", "-2147483648", "-2147483648", "-2147483648")
        elementLastDay = buildDate("lastDay", spec.lastYears[idx], spec.lastMonths[idx], spec.lastDays[idx], "0", "-2147483648", "-2147483648", "-2147483648")
        buildCaseCountCatgory(elementFirstArrayAxis, elementFirstDay, elementLastDay, spec.counts[idx])
    elementReferenceId = buildQualifiedElement("referenceId")
    elementReferenceId.text = "0"
    elementCaseCount.append(elementCaseCountArray)
    elementCaseCount.append(elementReferenceId)

def buildCaseCountCatgory(elementFirstArrayAxis, elementFirstDay, elementLastDay, countAsText):
    elementCategories = buildQualifiedElement("categories")
    elementCategoryDefinition = buildQualifiedElement("categoryDefinition")
    elementCategories.append(elementCategoryDefinition)
    elementOffsetFromUtcInHours = buildQualifiedElement("offsetFromUtcInHours")
    elementOffsetFromUtcInHours.text = "0"
    elementCategoryDefinition.append(elementOffsetFromUtcInHours)
    elementCategoryDefinition.append(elementFirstDay)
    elementCategoryDefinition.append(elementLastDay)
    elementCount = buildQualifiedElement("count")
    elementCount.text = countAsText
    elementCategories.append(elementCount)
    elementFirstArrayAxis.append(elementCategories)
    
def populateAppendTransmissionTrees(elementEpidemic, elementTransmissionTrees):
    elementEpidemic.append(elementTransmissionTrees)    
    
def populateAppendRelativeRiskDataSets(elementEpidemic, elementRelativeRiskDataSets):
    elementEpidemic.append(elementRelativeRiskDataSets)    
    
def populateAppendCausalPathogenIsolates(elementEpidemic, elementCausalPathogenIsolates):
    elementEpidemic.append(elementCausalPathogenIsolates)        
    
def populateAppendReferences(elementEpidemic, elementReferences):
    elementId = buildQualifiedElement("id")
    elementId.text = "0"
    elementReferences.append(elementId)
    elementTitle = buildQualifiedElement("title")
    elementTitle.text = "Number of Reported Cases of Diphtheria in Lebanon PA"
    elementReferences.append(elementTitle)
    elementPublication = buildQualifiedElement("publication")
    elementPublication.text = "Lebanon Gazette"
    elementReferences.append(elementPublication)
    elementUrl = buildQualifiedElement("url")
    elementUrl.text = "http://www.lebanon.org"
    elementReferences.append(elementUrl)
    elementEpidemic.append(elementReferences)    

def populateAppendEditHistory(elementEpidemic, elementEditHistory):
    elementEditHistory.text = "2015/03/21"
    elementEpidemic.append(elementEditHistory)
     
def testAgainstRest():     
    apolloRestConsumer = ApolloRestConsumer()
    responseString = apolloRestConsumer.consumeResponse("http://betaweb.rods.pitt.edu/apolloLibraryViewer-310-beta/api/v2/epidemic/7961.xml")
    responseTree = etree.XML(responseString)
    apolloXml = etree.tostring(responseTree, pretty_print=True)
    fo = open("a.xml", "wb")
    fo.write(apolloXml)
    fo.close()
    elementResourceResponse = buildResponseWrapper()
    tychoXml = etree.tostring(elementResourceResponse, pretty_print=True)
    fo = open("t.xml", "wb")
    fo.write(tychoXml)
    fo.close()
    if (tychoXml == apolloXml):
        print "EUREKA!"
    else:
        print "DRAT!"
 
def buildCaseCountSpecifierOne():
    caseCountSpecifier = CaseCountSpecifier()
    caseCountSpecifier.title = "Cumulative autochthonous confirmed (and probable) cases updated weekly since 2013"
    caseCountSpecifier.definitions.append("CONFIRMED_CASE")
    caseCountSpecifier.definitions.append("PROBABLE_CASE")
    caseCountSpecifier.arrayType = "CUMULATIVE_WITH_RESETS"
    caseCountSpecifier.firstArrayAxis = "TIME_SPAN"
    caseCountSpecifier.firstYears = ["2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013", "2015" ]
    caseCountSpecifier.firstMonths = ["12", "12", "12", "12", "12", "12", "12", "12", "12", "12", "1"]
    caseCountSpecifier.firstDays =   ["29", "29", "29", "29", "29", "29", "29", "29", "29", "29", "4"]
    caseCountSpecifier.lastYears = ["2014", "2014", "2014", "2014", "2014", "2014", "2014", "2014", "2014", "2015", "2015"]
    caseCountSpecifier.lastMonths = ["1", "1", "4", "5", "8", "9", "10", "11", "11", "1", "2" ]
    caseCountSpecifier.lastDays = ["4", "11", "26","24", "2", "27","25", "15", "29","3", "28"] 
    caseCountSpecifier.counts = [ "0", "0", "1", "4", "18", "18", "18", "18", "18", "18", "0"]
    return caseCountSpecifier

def buildCaseCountSpecifierTwo():
    caseCountSpecifier = CaseCountSpecifier()
    caseCountSpecifier.title = "Cumulative suspected cases updated weekly since 2013"
    caseCountSpecifier.definitions.append("EPIDEMIOLOGICALLY_LINKED_CASE")
    caseCountSpecifier.arrayType = "CUMULATIVE_WITH_RESETS"
    caseCountSpecifier.firstArrayAxis = "TIME_SPAN"
    caseCountSpecifier.firstYears =  ["2013", "2013", "2013", "2013", "2013", "2013", "2015" ]
    caseCountSpecifier.firstMonths = [  "12",   "12",   "12",   "12",   "12",   "12",    "1" ]
    caseCountSpecifier.firstDays =   [  "29",   "29",   "29",   "29",   "29",   "29",    "4" ]
    caseCountSpecifier.lastYears =   ["2014", "2014", "2014", "2014", "2014", "2015", "2015" ]
    caseCountSpecifier.lastMonths =  [   "8",    "9",   "10",   "11",   "11",    "1",    "2" ]
    caseCountSpecifier.lastDays =    [   "2",   "27",   "25",   "15",   "29",    "3",   "28" ] 
    caseCountSpecifier.counts =      [ "679", "1249", "1376", "1399", "1414", "1426",   "16" ]
    return caseCountSpecifier

def buildCaseCountSpecifierThree():
    caseCountSpecifier = CaseCountSpecifier()
    caseCountSpecifier.title = "Cumulative fatal cases updated weekly since 2013"
    caseCountSpecifier.definitions.append("FATAL_CASE")
    caseCountSpecifier.arrayType = "CUMULATIVE_WITHOUT_RESETS"
    caseCountSpecifier.firstArrayAxis = "TIME_SPAN"
    caseCountSpecifier.firstYears =  ["2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013", "2013" ]
    caseCountSpecifier.firstMonths = [  "12",   "12",   "12",   "12",   "12",   "12",   "12",   "12",   "12",   "12" ]
    caseCountSpecifier.firstDays =   [  "29",   "29",   "29",   "29",   "29",   "29",   "29",   "29",   "29",   "29" ]
    caseCountSpecifier.lastYears =   ["2014", "2014", "2014", "2014", "2014", "2014", "2014", "2014", "2014", "2015" ]
    caseCountSpecifier.lastMonths =  [   "1",    "1",    "4",    "5",    "8",     "9",   "10",   "11",  "11",    "1" ]
    caseCountSpecifier.lastDays =    [   "4",   "11",   "26",   "24",    "2",    "27",   "25",   "15",  "29",    "3" ] 
    caseCountSpecifier.counts =      [   "0",    "0",    "0",    "0",     "0",    "0",    "0",    "0",   "0",    "0" ]
    return caseCountSpecifier

    
generateXmlQueryResponse()
#trialValidation()
    