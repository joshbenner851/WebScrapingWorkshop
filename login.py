import http.cookiejar as cookielib
import os
import urllib
import re
import string
from bs4 import BeautifulSoup, SoupStrainer
import time

username = "bennerster@gmail.com"
password = "cak851e"

cookie_filename = "parser.cookies.txt"

class LinkedInParser(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password

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

        title = self.loadTitle()
        print(title)

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
            return self.loadPage(url, data)

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
        soup = self.loadSoup("https://www.linkedin.com/")
#        csrf = "df134269-02ba-4db0-814a-d358bddccdd9"
        #csrf = soup.find(id="loginCsrfParam-login")['value']
        login_data = urllib.parse.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': "efc748d7-5fb4-496a-852d-bf421111ad5b",
        }).encode('utf8')

        self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return

    def loadTitle(self):
        #find the number of members...
        #members = soup.loadSoup().find
        members = 3553
        pages = (members/50) + 1
        users = 0
        '''for x in range(0,10):
            soup = self.loadSoup("https://www.linkedin.com//manageGroupMembers?dispParts=&gid=1946872&memberLevel=MEMBER&sort=lna&split_page=" + str(x))
            #grabbing all the prole links of users, still need to grab their public 
            print(soup.find("title"))
            for a in soup.find_all('a', href=True):
                if(("https://www.linkedin.com/profile/view?id=" in a['href']) and ("mem_prof" in a['href'])):
                    users += 1
                    print("Found the URL, user" + str(users) + ":", a['href'])
            time.sleep(10)
            '''
        soup = self.loadSoup("https://www.linkedin.com/manageGroupMembers?dispParts=&gid=1946872&memberLevel=MEMBER")
        #soup = self.loadSoup("https://www.linkedin.com/grp/home?gid=1946872")
        #soup = self.loadSoup("https://www.linkedin.com//manageGroupMembers?dispParts=&gid=1946872&memberLevel=MEMBER&sort=lna&split_page=1")
        strongs = soup.find_all('strong')
        for people in strongs:
            if people:
                if len(people.contents) > 1:
                    text = people.contents[1]
                    print(text.text)

        #print(soup.select('strong a[href*=https://www.linkedin.com/profile/view?id=]'))
        '''print(soup.findAll('div',{'class':'content-wrapper'})[0].text)
        print()
        print(soup.findAll('div',{"class":"right-entity"})[0].text)
        print()
        print()
        print(soup.findAll('div',{"class":"member-count identified"}))'''
        return soup.find("title")

def grabUrl(url):
    req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    return html

def grabUsersUrls(html):
    soup = BeautifulSoup(html,"html.parser")
    #urls = soup.findAll('a').text
    #print(urls)
    
    
    
parser = LinkedInParser(username, password)


