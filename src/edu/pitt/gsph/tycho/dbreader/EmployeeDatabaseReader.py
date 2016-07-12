'''
Created on Jun 9, 2016

@author: kjm84
'''

#
# Useful list functions
#
# cmp(list1, list2)
# len(list)
# max(list)
# min(list)
# list(seq)
# list.append(obj)
# list.count(obj)
# list.extend(seq)
# list.index(obj)
# list.insert(index, obj)
# list.pop(obj=list[-1])
# list.remove(obj)
# list.reverse()
# list.sort([func])
 

#
# Useful dictionary functions
#
# cmp(dict1, dict2)
# len(dict)
# str(dict)
# type(variable)
# dict.clear()
# dict.copy()
# dict.fromkeys()
# dict.get(key, default=None)
# dict.has_key(key)
# dict.items()
# dict.keys()
# dict.setdefault(key, default=None)
# dict.update(dict2)
# dict.values()

import MySQLdb
from Employee import Employee
from OOP import Child
from OOP import Vector
from OOP import JustCounter

if __name__ == '__main__':
    pass

employeeDict = {}
def attrManipulation(emp):
    hasAge = hasattr(emp, 'age')           # Returns true if 'age' attribute exists
    ageValue = getattr(emp, 'age')         # Returns value of 'age' attribute
    setattr(emp, 'age', 8)                 # Set attribute 'age' at 8
    updatedAgeValue = getattr(emp, 'age')  # Returns new value of 'age' attribute
    delattr(emp, 'age')                    # Delete attribute 'age'
    updatedHasAge = hasattr(emp, 'age')    # Returns false because 'age' no longer exists
    print "hasAge=%s,ageValue=%d,newAgeValue=%d,updatedHasAge=%s" % \
                 (hasAge, ageValue, updatedAgeValue, updatedHasAge )
  
def employeeObjectTests():
    emp1 = Employee("Zara", "Zara", 27, 'F', 2000)
    emp2 = Employee("Clara", "Clara", 31, 'M', 10000)
    emp1.displayCount()
    emp1.displayEmployee()
    emp2.displayCount()
    emp2.displayEmployee()
    attrManipulation(emp2)
    emp1.displayEmployeeMetaInfo()

def performOopTests():    
    c = Child()          # instance of child
    c.childMethod()      # child calls its method
    c.parentMethod()     # calls parent's method
    c.setAttr(200)       # again call parent's method
    c.getAttr()          # again call parent's method
    c.myMethodForOverriding()
    v1 = Vector(2,10)
    v2 = Vector(5,-2)
    print v1 + v2
    counter = JustCounter()
    counter.count()
    counter.count()
    print counter._JustCounter__secretCount
    
def displayVersion(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print "Database version : %s " % data
    
def executeUpdate(db, sql):
    cursor = db.cursor()
    try:        
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
 
def createOrReplaceEmployees(db):    
    executeUpdate(db, "DROP TABLE IF EXISTS EMPLOYEE")
    sql = """CREATE TABLE EMPLOYEE (
         id BIGINT NOT NULL AUTO_INCREMENT,
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT,
         PRIMARY KEY (id))
        """
    executeUpdate(db, sql)

def findLowIncomeIndividuals(db):
    sql = "SELECT id, FIRST_NAME, LAST_NAME, AGE, SEX, INCOME FROM EMPLOYEE \
       WHERE INCOME < '%d'" % (10000)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print "Low income individuals list:"
        for row in results:
            employeeId = row[0]
            fname = row[1]
            lname = row[2]
            age = row[3]
            sex = row[4]
            income = row[5]
            print "id=%d,fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                 (employeeId,fname, lname, age, sex, income )
    except:
        print "Error: unable to fecth data"
        
def updateExampleOne(db):
    sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 \
                          WHERE SEX = '%c'" % ('M')
    executeUpdate(db, sql)
    
def deleteExampleOne(db):
    sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (25)
    executeUpdate(db, sql)
    
def insertEmployeeExampleOne(db):
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    executeUpdate(db, sql)
    
def insertEmployeeExampleTwo(db):
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
       ('Mary', 'Mohan', 22, 'F', 1998)
    executeUpdate(db, sql)
     
def insertEmployeeExampleThree(db):
    firstName = "Freddie"
    lastName = "Freeloader"
    cursor = db.cursor()
    try:
        cursor.execute('insert into employee (FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) values("%s", "%s", "%d", "%c", "%d")' % \
             (firstName, lastName, 48, 'M', 0))
        db.commit()
    except:
        print "failed to insert Freddie"
        db.rollback()

def insertEmployees(db):
    insertEmployeeExampleOne(db)
    insertEmployeeExampleTwo(db)
    insertEmployeeExampleThree(db)
         
def cacheEmployees(db):
    sql = "SELECT id, FIRST_NAME, LAST_NAME, AGE, SEX, INCOME FROM EMPLOYEE"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            emp = Employee(row[0],row[1],row[2],row[3],row[4],row[5])
            employeeDict[emp.employeeId] = emp
    except:
        print "Error: unable to fecth employee data"

def performEmployeeCaching(db):
    displayVersion(db)
    createOrReplaceEmployees(db)
    insertEmployees(db)
    cacheEmployees(db)
    print employeeDict.keys()
    for employeeId in employeeDict.keys():
        emp = employeeDict[employeeId]
        emp.displayEmployee()

def performDbTests():
    db = MySQLdb.connect("localhost","*","*", "*", 3308)
    performEmployeeCaching(db)
    db.close()
    
performDbTests()



