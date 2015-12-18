import urllib2
import urllib
from bs4 import BeautifulSoup

from NewsPage import *


def getAllNews():
    baseUrl = 'http://www.dndi.org/category/media-centre/news/page/'
    
    pageNum = 1
    result = []
    while ( True ):
    
        url = baseUrl + str(pageNum) + '/'
        data = urllib.urlencode( {} )
        headers = {}
        request = urllib2.Request( url, data, headers )
        
        try:
            response = urllib2.urlopen( request )
        except urllib2.HTTPError as e:
            if e.code == 404:
                break;
            else:
                print('unexpected error occured')
                
        pageSource = response.read()
        
        text = BeautifulSoup( pageSource, "html.parser" )
        
        articles = text.find_all( 'article' )
        
        urls = []
        for article in articles:
            anchor = article.find( 'a', href=True )
            urls.append( anchor['href'] )
    
        i = 1
        for url in urls:
            result.append( getNewsPage( url ) )
            print( str(i) + ' in ' + str( len(urls) ) + ' is done!' )
            i = i + 1
        pageNum = pageNum + 1
    return result
