import http.cookiejar as cookielib
import os
import urllib
import re
import string
from bs4 import BeautifulSoup, SoupStrainer
import time
import requests

email = "bennerster@gmail.com"
firstName = "Josh"
lastName = "Benner"
stuff = "b_428a7e16740ac4c2e3533292d_18414bad83"

cookie_filename = "parser.cookies.txt"

class SpartanHackersParser(object):

    def __init__(self, email, first, last, code):
        """ Start up... """
        self.email = email
        self.first = first
        self.last = last
        self.code = code
        self.subscribe = ""

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # Login
        self.loginPage()

        self.cj.save()


    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join([str(l) for l in response.readlines()])
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            #return self.loadPage(url, data)
            print("fail")

    def loadSoup(self, url, data=None):
        """
        Combine loading of URL, HTML, and parsing with BeautifulSoup
        """
        html = self.loadPage(url, data)
        soup = BeautifulSoup(html)
        '''for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
            if link.has_attr('href'):
                print(link['href'])'''
        #print(urls)
        return soup

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        soup = self.loadSoup("http://spartanhackers.com/")
#        csrf = "df134269-02ba-4db0-814a-d358bddccdd9"
        #csrf = soup.find(id="loginCsrfParam-login")['value']
        login_data = urllib.parse.urlencode({
            'EMAIL': self.email,
            'FNAME': self.first,
            'LNAME': self.last,
            'MMERGE3': "No",
        }).encode('utf8')

        self.loadPage("/spartanhackers.us11.list-manage.com/subscribe/post?u=c4c0006c6308da6ea656d3c03&id=53f0c18efe", login_data)
        return

def grabUrl(url):
    req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    return html

def grabUsersUrls(html):
    soup = BeautifulSoup(html, "html.parser")
    #urls = soup.findAll('a').text
    #print(urls)
    
parser = SpartanHackersParser(email, firstName, lastName, stuff)


