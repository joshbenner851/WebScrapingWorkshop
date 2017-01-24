import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time


url = "https://eatatstate.com/menus/brody"
req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html)

# grabs all the view-content tags, we want the first one
viewContent = soup.find_all("div", class_="view-content")[1]
# print(viewContent)

# each dining place is in a table, so lets iterate over those
for tables in viewContent.contents:
    #print(tables)
    # if the table isn't empty and isn't a new line character
    if tables and tables != '\n':
        # scraping is weird and inserts new line characters into lists
        #  so the body is actually the fifth spot in the array
        # print(tables.contents)
        body = tables.contents[5]
        # print(body)
        # grab oddview and filter out new line character
        oddView = [x for x in body.contents if x!='\n']
        # filter new line character again
        menuValue = [a for a in oddView if a!='\n']
        # print(menuValue)
        # now lets grab all the menu values
        for value in menuValue:
            # filter again
            itemLst = [x for x in value.contents if x != '\n']
            # print(itemLst)
            # for every item in the food values
            for item in itemLst:
                # filter list
                lst = [a for a in item.contents if a != '\n']
                # print(lst)
                if lst:
                    # every food item
                    for food in lst:
                        if('\n' not in food):
                            if food != " ":
                                # prints each field items
                                a = 5
                                print(food.text)
                                
        print()
        print()
