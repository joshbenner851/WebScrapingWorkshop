import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


url = "https://eatatstate.com/menus/brody"
req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html)


#print(soup.title)
#print(soup.p)
#print(soup.a)
#print(soup.find_all('a'))

date = soup.find_all('div',class_="date-heading")
print(date)
#viewContent = soup.find_all("div",class_="view-content")[1]

# for tables in viewContent.contents:
# 	if tables and tables != "/n":
# 	    body = tables.contents[5]
# 	    oddView = [x for x in body.contents if x!='\n']
# 	    print(oddView)





