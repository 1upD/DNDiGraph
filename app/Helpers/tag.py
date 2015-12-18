# coding= utf-8

import mysql.connector

connection = mysql.connector.connect(user='root', database='dndi', password='cs300')
cursor = connection.cursor()
 
addStatment = ( "INSERT INTO tag ( id, name ) VALUES( %s, %s )" )

tags = [ 'HAT - Sleeping Sickness', 'Chagas disease', 'Filarial diseases', 'Hepatitis C', 'Leishmaniasis', 'Malaria', 'Mycetoma',
        'Paediatric HIV', 'Access', 'Advocacy', 'Funding', 'Partnership', 'Regulatory', 'Strengthening capacities', 'Treatment' ]
  
i = 0
for tag in tags:
    dataStatement = ( i, tag )
    cursor.execute( addStatment, dataStatement )
    i = i + 1
connection.commit()