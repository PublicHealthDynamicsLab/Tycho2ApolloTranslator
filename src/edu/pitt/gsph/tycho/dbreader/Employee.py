'''
Created on Jun 9, 2016

@author: kjm84
'''

class Employee:
    
    'Common base class for all employees'
   
    empCount = 0

    def __init__(self, employeeId, firstName, lastName, age, gender, income):
        self.employeeId = employeeId
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.gender = gender
        self.income = income
        Employee.empCount += 1
        
    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "destroyed"    
   
    def displayCount(self):
        print "Total Employee %d" % Employee.empCount

    def displayEmployee(self):
        print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                 (self.firstName, self.lastName, self.age, self.gender, self.income)
                 

    def displayEmployeeMetaInfo(self):
        print "Employee.__doc__:", Employee.__doc__
        print "Employee.__name__:", Employee.__name__
        print "Employee.__module__:", Employee.__module__
        print "Employee.__bases__:", Employee.__bases__
        print "Employee.__dict__:", Employee.__dict__  