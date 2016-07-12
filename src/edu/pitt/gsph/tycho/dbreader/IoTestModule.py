'''
Created on Jun 27, 2016

@author: kjm84
'''
import os 
import shutil

if __name__ == '__main__':
    pass

def inputExamples():
    inputString = raw_input("Enter your input: ");
    print "Received input is : ", inputString
    # 'x*5 for x in range(2,10,2)'    
    inputString = input("Enter your input: ");
    print "Received input is : ", inputString

def writeFileExample():
    fo = open("foo.txt", "wb")
    print "Name of the file: ", fo.name
    fo.write( "Python is a great language.\nYeah its great!!\n");
    fo.close()

def readFileExample():
    inputFile = open("foo.txt", "r+")
    inputLines = inputFile.read(10);
    print "Read String is : ", inputLines
    inputFile.close()
    
def readFileExample2():
    fo = open("foo.txt", "r+")
    inputString = fo.read(10);
    print "Read String is : ", inputString
    position = fo.tell();
    print "Current file position : ", position
    position = fo.seek(0, 0);
    inputString = fo.read(10);
    print "Again read String is : ", inputString
    fo.close()
    
def readBrazilZikaOutputXml():
    inputFile = open("../Brazil_Zika_Output.xml", "r+")
    inputLines = inputFile.read(10)
    print "Read String is : ", inputLines
    inputFile.close()
    
def osExamples():
    os.rename( "foo.txt", "foo2.txt" )
    inputFile = open("foo2.txt", "r+")
    outputFile = open("foo.txt", "w")
    shutil.copyfileobj(inputFile, outputFile)
    inputFile.close()
    outputFile.close()
    os.remove("foo2.txt")
  
def combinedExamples():   
    osExamples()  
    readFileExample2()
    readBrazilZikaOutputXml()
    
#writeFileExample()


