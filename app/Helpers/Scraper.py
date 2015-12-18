from bs4 import BeautifulSoup
import urllib
import urllib2
'''
Created on Dec 16, 2015

@author: Derek Dik
'''
from ScientificArticle import ScientificArticle
from WebScraperUtils import monthAndYear
from PressRelease import PressRelease

class Scraper(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._soup = None 
        self._pages = list()
        self._releases = list()
        self._articles = list()
    def load_page(self, URL):
        html_doc = urllib2.urlopen(URL)
        self._soup = BeautifulSoup(html_doc, "html.parser")
        
    def find_releases(self):
        print("Loading releases...")
        count = 0
        for page in self._pages:
            text = BeautifulSoup( page, "html.parser" )
            article_headers = text.find_all( 'article' )
            for article_header in article_headers:
                anchor = article_header.find( 'a', href=True )
                article_url = anchor['href']
                article_summary = article_header.find_all( 'div', class_= 'entry-summary')[0].get_text().strip()
                article_words = article_summary.split()
                article = PressRelease(article_url)
                article.scrape()
                self._releases.append(article)
                count += 1
                print("Releases Processed: " + str(count))
        print(str(count) + " releases loaded!")
        
    def find_articles(self):
        print("Loading articles...")
        count = 0
        for page in self._pages:
            text = BeautifulSoup( page, "html.parser" )
            article_headers = text.find_all( 'article' )
            for article_header in article_headers:
                anchor = article_header.find( 'a', href=True )
                article_url = anchor['href']
                article_summary = article_header.find_all( 'div', class_= 'entry-summary')[0].get_text().strip()
                article_words = article_summary.split()
                datestr = monthAndYear(article_words[-2], article_words[-1])
                article = ScientificArticle(article_url, datestr)
                article.scrape()
                self._articles.append(article)
                count += 1
                print("Articles Processed: " + str(count))

        print(str(count) + " articles loaded!")
    def load_pages(self, URL):
        print("Finding pages...")
        # Count up page numbers from one
        page = 1
        # Loop indefinitely until break
        while True:
            # Set the next page URL to be the given URL plus the page number
            next_page_URL = URL + str(page)
            # Opening the page will raise an exception if the page does not exist
            try:
                # Open the page
                next_page = urllib2.urlopen(next_page_URL).read()
                # Add the HTML to the list of pages
                self._pages.append(next_page)
                # 
            # If an exception is caught, assume all pages have been read
            except urllib2.HTTPError as e:
                break
            # Increment page count
            page += 1
        print(str(page) + " Pages Loaded!")    
        
    
