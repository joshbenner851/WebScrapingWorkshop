# WebScrapingWorkshop




import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

#url of the site we're scraping
url = "https://eatatstate.com/menus/brody"
req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
#Creating the BeautifulSoup object
soup = BeautifulSoup(html)






