'''
Created on Jun 8, 2016

@author: kjm84
'''

import MySQLdb
import Disease

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

def buildDiseaseQuery(diseaseName):
    return "select \
           d.id as diseaseId, d.name as diseaseName, ds.id as diseaseSubcategoryId, ds.name as diseaseSubcategoryName \
           from disease d left join disease_subcategory ds on d.id = ds.disease_id \
           where d.name like '%s'" % (diseaseName)
    
def tryFindDiseaseAndDiseaseSubcategories(db, diseaseName):
    cursor = db.cursor()
    cursor.execute(buildDiseaseQuery(diseaseName))
    results = cursor.fetchall()
    for row in results:
        disease = Disease(row[0], row[1], row[2], row[3])
        break
    return disease
    
def findDiseaseAndDiseaseSubcategories(db, diseaseName):
    sql = buildDiseaseQuery(diseaseName)
    print sql
    try:
        disease = tryFindDiseaseAndDiseaseSubcategories(db, sql)
        disease.display()
    except:
        print "Error: fetching and parsing disease data"  
    
#
# Main code here
#
sql = "select year, week, number from weekly_reported_counts where location_id = 3313 and dis_sub_id = 14 order by year, week"
db = MySQLdb.connect("localhost","***","***","***", 3308 )
disease = tryFindDiseaseAndDiseaseSubcategories(db, "DIPHTHERIA")
disease.display()
db.close()
