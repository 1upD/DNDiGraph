# coding= utf-8

from bs4 import BeautifulSoup
from Event import *
from News import *
from IntheMedia import *
import mysql.connector
import time
from Scraper import Scraper

def toDict(article):
    result = {}
    result[ 'id' ] = article._id
    result[ 'title' ] = article._title
    result[ 'tag' ] = article._tags
    result[ 'category'] = article._cats
    result[ 'body' ] = article._body
    result[ 'url' ] = article._url
    result[ 'date' ] = article._datestr
    return result 

class DNDiDB:
    TAGS = [ 'HAT – Sleeping Sickness', 'Chagas disease', 'Filarial diseases', 'Hepatitis C', 'Leishmaniasis', 'Malaria', 'Mycetoma',
        'Paediatric HIV', 'Access', 'Advocacy', 'Funding', 'Partnership', 'Regulatory', 'Strengthening capacities', 'Treatment' ]
    
    MONTH = { 'January': '01', 'February': '02', 'March': '03', 'April': '04','May': '05','June': '06',
            'July': '07','August': '08','September': '09','October': '10','November': '11','December': '12'}
    def __init__(self, tables ):
        self.tables = tables
        self.connection = mysql.connector.connect(user='root', database='dndi', password='cs300')
        self.cursor = self.connection.cursor()

    def deleteALL(self):
        for table in self.tables:
            self.cursor.execute( ( "delete from " + table ) )
        self.cursor.execute( ( "delete from tagPost" ) )
        self.connection.commit()
        
    def importTable( self, table ):
        addStatment = ( "INSERT INTO " + table + " ( id, title, date, body, url, category ) VALUES( %s, %s, %s, %s, %s, %s )" )
        tagStatement = ( "INSERT INTO tagPost ( tag_id, post_id ) VALUES( %s, %s )" )
        data = self.getData( table )
        
        if data is not False:
            for datum in data:
                date = self._getDate( datum['date'] )
                dataStatement = ( datum['id'],datum['title'],date,datum['body'],datum['url'],datum['category'])
                for tag in datum['tag']:
                    if tag[:3] == 'HAT':
                        tagID = 0
                    else:
                        tagID = self.TAGS.index(tag)
                    try:
                        self.cursor.execute( tagStatement, ( tagID, datum['id'] ) )
                    except Exception as e:  
                        if e.errno == 1406:
                            dataStatement = ( datum['id'],datum['title'][0:200], None, datum['body'],datum['url'],datum['category'])
                            self.cursor.execute( addStatment, dataStatement )
                try:
                    self.cursor.execute( addStatment, dataStatement )
                except Exception as e:
                    if e.errno == 1292:
                        dataStatement = ( datum['id'],datum['title'], None, datum['body'],datum['url'],datum['category'])
                        self.cursor.execute( addStatment, dataStatement )
                    else:
                        print(datum)
                    logging.exception( datum )
            self.connection.commit()
            
        print(table + ' is commited!')
        
    def getData( self, table ):
        if table == 'Event':
            return getAllEvent()
        elif table == 'News':
            return getAllNews()
        elif table == 'InTheMedia':
            return getAllInTheMedia()
        elif table == 'ScientificArticle':
            scraper = Scraper()
            scraper.load_pages("http://www.dndi.org/category/media-centre/scientific-articles/page/")
            scraper.find_articles()
            result = []
            for article in scraper._articles:
                result.append( toDict(article) )
            return result
        elif table == 'PressRelease':
            scraper = Scraper()
            scraper.load_pages("http://www.dndi.org/category/media-centre/press-releases/page/")
            scraper.find_releases()
            result = []
            for article in scraper._releases:
                result.append( toDict(article) )
            return result
        else:
            return False
        
    def importAll(self):
        for table in self.tables:
            self.importTable( table )
            
    def _getDate(self, string):
        string = string.strip()
        string = string.replace('[', '')
        string = string.split(']')[0]
        string = string.replace(',', '').strip()
        array = string.split(' ')
        if len( array ) == 1:
            if array[0].isdigit():
                return array[0] + '-00-00'
            else:
                return None
        elif len( array ) == 2:
            if self.MONTH.has_key( array[ 0 ] ):
                month = self.MONTH[ array[0] ]
            else:
                month = '00'
            return array[-1] + '-' + month + '-00'
        else:
            if array[0].split('-')[0].isdigit():
                date = array[0]
                if self.MONTH.has_key( array[ 1 ] ):
                    month = self.MONTH[ array[ 1 ] ]
                else:
                    month = '00'
            else:
                date = array[1]
                if self.MONTH.has_key( array[ 0 ] ):
                    month = self.MONTH[ array[ 0 ] ]
                else:
                    month = '00'
            if len(date) > 1:
                if not date[1].isdigit():
                    date = '0' + date[0]
            return array[-1] + '-' + month + '-' + date[:2]
            
start_time = time.time()

dndi = DNDiDB( [ 'Event', 'News', 'InTheMedia', 'ScientificArticle', 'PressRelease' ] )
dndi.deleteALL()
dndi.importAll()

print('Total Elapsed: ' + str( time.time() - start_time ) )