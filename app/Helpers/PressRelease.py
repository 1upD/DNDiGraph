'''
Created on Dec 16, 2015

@author: Derek Dik
'''

import urllib
from bs4 import BeautifulSoup
from WebScraperUtils import formatString, monthAndYear
import urllib2

class PressRelease(object):
    '''
    classdocs
    '''


    def __init__(self, URL):
        '''
        Constructor
        '''
        self._url = URL
        self._title = ""
        self._tags = ""
        self._cats = ""
        self._body = ""
        self._datestr = ""
        self._id = ""
                
    def scrape(self):
        try:
            pageSource = urllib2.urlopen(self._url).read()
            
            text = BeautifulSoup( pageSource, "html.parser" ).find('article')
            self._id = text.get( 'id' )
            try:
                self._title = text.find_all( 'h1', class_= 'entry-title')[0].get_text().strip()
            except Exception as e:
                print(e)
                print("No title found.")
            try:
                self._cats = text.find_all( 'span', class_= 'cat-links')[0].get_text().strip()
            except Exception as e:
                print(e)
                print("No categories found.")
            
            self._tags = list()
            # If an exception is caught, then there are no tags
            try:
                tags_str = text.find_all( 'span', class_= 'tag-links')[0].get_text().strip()
                tags_split = tags_str.split(",")
                for tag in tags_split:
                    self._tags.append(tag.lstrip())
            except Exception as e:
                print(e)
                print("No tags found.")

            try:
                self._body = formatString( text.find_all( 'div', class_='entry-content')[0].get_text().strip() )
            except Exception as e:
                print(e)
                print("No body found.")
            try:
                date_split = text.find_all( 'span', class_= 'date-press')[-1].get_text().split()
                
                datestr = monthAndYear(date_split[-2], date_split[-1])
                if datestr == "":
                    urlYear = self._url[20:24]
                    self._datestr = monthAndYear("", urlYear)
                else:
                    self._datestr = datestr
            except Exception as e:
                print(e)
                print("Exception: No date found. Using URL")
                urlYear = self._url[20:24]
                self._datestr = monthAndYear("", urlYear)
            
        except urllib2.URLError as e:
            print(e)
            print("Could not load URL")