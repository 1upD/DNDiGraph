'''
Created on Dec 16, 2015

@author: Derek Dik
'''

import urllib
import urllib2
from bs4 import BeautifulSoup
from WebScraperUtils import formatString, monthAndYear

class ScientificArticle(object):
    '''
    classdocs
    '''


    def __init__(self, URL, datestr):
        '''
        Constructor
        '''
        self._url = URL
        self._title = ""
        self._tags = ""
        self._cats = ""
        self._body = ""
        self._id = ""
        if datestr == "":
            urlYear = self._url[20:24]
            self._datestr = monthAndYear("", urlYear)
        else:
            self._datestr = datestr
    
    def scrape(self):
        try:
            pageSource = urllib2.urlopen(self._url).read()
            
            text = BeautifulSoup( pageSource, "html.parser" ).find('article')
            self._id = text.get( 'id' )
            self._title = text.find_all( 'h1', class_= 'entry-title')[0].get_text().strip()
            self._tags = list()
            # If an exception is caught, then there are no tags
            try:
                tags_str = text.find_all( 'span', class_= 'tag-links')[0].get_text().strip()
                tags_split = tags_str.split(",")
                for tag in tags_split:
                    self._tags.append(tag.lstrip())
            except Exception as e:
                print(e)
            self._cats = 'scientificArticle'
            self._body = formatString( text.find_all( 'div', class_='entry-content')[0].get_text().strip() )
        except urllib2.URLError as e:   
            print(e)