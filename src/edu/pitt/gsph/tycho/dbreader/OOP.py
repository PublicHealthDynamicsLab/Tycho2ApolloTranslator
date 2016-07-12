'''
Created on Jun 9, 2016

@author: kjm84
'''

#
# __init__ ( self [,args...] )
# Constructor (with any optional arguments)
# Sample Call : obj = className(args)
#
#__del__( self )
# Destructor, deletes an object
# Sample Call : del obj
#
#  __repr__( self )
# Evaluatable string representation
# Sample Call : repr(obj)
#
#    __str__( self )
# Printable string representation
# Sample Call : str(obj)
#
# __cmp__ ( self, x )
# Object comparison
# Sample Call : cmp(obj, x)
#

class Parent:
    
        parentAttr = 100

        def __init__(self):
            print "Calling parent constructor"

        def parentMethod(self):
            print 'Calling parent method'

        def setAttr(self, attr):
            Parent.parentAttr = attr

        def getAttr(self):
            print "Parent attribute :", Parent.parentAttr
            
        def myMethodForOverriding(self):
            print 'Calling parent overridden method'


class Child(Parent):
    
    def __init__(self):
        print "Calling child constructor"
        
    def childMethod(self):
        print 'Calling child method'
    
    def myMethodForOverriding(self):
        print 'Calling child overridden method'
        
class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)
   
    def __add__(self,other):
        return Vector(self.a + other.a, self.b + other.b)

class JustCounter:
    __secretCount = 0
  
    def count(self):
        self.__secretCount += 1
        print self.__secretCount
