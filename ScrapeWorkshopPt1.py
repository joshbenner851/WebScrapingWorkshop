import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


url = "https://eatatstate.com/menus/brody"
req = urllib.request.Request(url, None, headers={'User-Agent' : 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html, "html.parser")

# grabs page title
print("title: ", soup.title)

# grabs first paragraph
print("paragraph: ", soup.p)

# grabs first anchor tag(link)
print("anchor tag: ", soup.a)

# grabs all anchor(link tags) -> extremely useful to grab all the links on a page
print("all links: ", soup.find_all('a'))


date = soup.find_all('div', class_="date-heading")
print("data: ", date)

print()
print()
print()

viewContent = soup.find_all("div", class_="view-content")[1]
print(viewContent)

# for tables in viewContent.contents:
# 	if tables and tables != "/n":
#     	    body = tables.contents[5]
#     	    oddView = [x for x in body.contents if x!='\n']
#     	    print(oddView)
#     #





