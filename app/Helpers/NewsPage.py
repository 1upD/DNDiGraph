import urllib2
import urllib
from bs4 import BeautifulSoup

def formatString( string ):
    result = ''
    for char in string:
        if char == '\n':
            if result[ -1 ] != '\n':
                result = result + char
        else:
            result = result + char
    return result

def getNewsPage( url ):
    data = urllib.urlencode( {} )
    headers = {}
    request = urllib2.Request( url, data, headers )
    pageSource = urllib2.urlopen( request ).read()
    
    text = BeautifulSoup( pageSource, "html.parser" )

    title = text.find( 'h1', class_= 'entry-title').get_text().strip()
    
    date = text.find( 'time', class_= 'entry-date').get_text().strip()
    
    body = formatString( text.find( 'div', class_='entry-content').get_text().strip() )
    footer = text.find( 'footer', class_= 'entry-footer')
    
    catLink = footer.find( 'span',class_="cat-links" ).get_text().strip()
    tagLink = footer.find( 'span',class_="tag-links" )
    tags = []
    if tagLink is not None:
        tagLink = tagLink.get_text()
        
        for tag in tagLink.split(','):
            tags.append(tag.strip())
    id = text.find( 'article' ).get( 'id' )
        
    result = {}
    result[ 'title' ] = title
    result[ 'date' ] = date
    result[ 'body' ] = body
    result[ 'url' ] = url
    result[ 'category' ] = catLink
    result[ 'tag' ] = tags
    result[ 'id' ] = id
    
    return result