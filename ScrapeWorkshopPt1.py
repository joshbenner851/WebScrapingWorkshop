import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


url = "https://eatatstate.com/menus/brody"
req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html)

# grabs page title
# print(soup.title)

# grabs first paragraph
# print(soup.p)

# grabs first anchor tag(link)
# print(soup.a)

# grabs all anchor(link tags) -> extremely useful to grab all the links on a page
# print(soup.find_all('a'))


date = soup.find_all('div',class_="date-heading")
#
viewContent = soup.find_all("div",class_="view-content")[1]

# for tables in viewContent.contents:
# 	if tables and tables != "/n":
#     	    body = tables.contents[5]
#     	    oddView = [x for x in body.contents if x!='\n']
#     	    print(oddView)
#     #




