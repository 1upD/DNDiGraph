import urllib2
import urllib
from bs4 import BeautifulSoup
from progressBar import *
import logging

def getAllInTheMedia():

    baseUrl = 'http://www.dndi.org/category/media-centre/in-the-media/page/'
    pageNum = 1
    results = []
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
                print( 'hi')
            else:
                print('unexpected error occured')
                
        pageSource = response.read()
        
        text = BeautifulSoup( pageSource, "html.parser" )
        
        articles = text.find_all( 'article' )
        
        i = 1
        print( 'working on page' + str( pageNum ))
        for article in articles:
            try:
                content = article.find( 'div', class_='entry-content' )
                result = {}
                date = content.find( 'span', 'date-press' )
                
                if date is None:
                    date = content.find( 'span', 'date' )
                    if date is None:
                        date = content.find( 'span', 'texte_bleu' ).replaceWith('').get_text()
                    else:
                        date = date.replaceWith('').get_text()
                else:
                    date = date.replaceWith('').get_text()
                
                result[ 'date' ] = date
                
                title = content.find( 'h2' )
                
                if title is None:
                    title = content.find('span', class_='titre2').get_text().strip()
                else:
                    title = content.find( 'h2' ).get_text().strip()
                    
                result[ 'title' ] = title
                
                body = content.find( 'h3' )
                
                if body is None:
                    body = content.find('span', class_='titre3').get_text().strip()
                else:
                    body = body.get_text().strip()
                
                result[ 'body' ] = body
                
                result[ 'url' ] = content.find( 'a', href=True )[ 'href' ]
                
                footer = article.find( 'footer', class_= 'entry-footer')
                catLink = footer.find( 'span',class_="cat-links" ).get_text().strip()
                tagLink = footer.find( 'span',class_="tag-links" )
                tags = []
                if tagLink is not None:
                    tagLink = tagLink.get_text()
                    
                    for tag in tagLink.split(','):
                        tags.append(tag.strip())
                        
                result[ 'tag' ] = tags
                result[ 'category' ] = catLink
                
                result[ 'id' ] = article.get('id')
                
                i = i + 1
                results.append(result)
            except ( TypeError, AttributeError ) as error:
                logging.exception( 'pageNum is ' + str(pageNum) + ' and ' + 'i is ' + str(i) )
        pageNum = pageNum + 1
    return results