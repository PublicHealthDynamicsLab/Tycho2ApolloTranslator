'''
Created on Jun 9, 2016

@author: kjm84
'''

class Disease:
    
    'Common base class for all diseases'
   
    diseaseCount = 0

    def __init__(self, diseaseId, diseaseName, diseaseSubcategoryId, diseaseSubcategoryName):
        self.diseaseId = diseaseId
        self.diseaseName = diseaseName
        self.diseaseSubcategoryId = diseaseSubcategoryId
        self.diseaseSubcategoryName = diseaseSubcategoryName
   
    def displayCount(self):
        print "Total Disease Count is %d" % Disease.diseaseCount

    def display(self):
        print "id: ", self.id, "name: ", self.name, "scId: ", self.subcategoryId, "scName: ", self.subcategoryName 
        
    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "destroyed"    