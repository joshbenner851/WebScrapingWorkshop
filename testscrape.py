import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time

def grabFoodPage(date):
    #paginating
    for x in range(0,2):
        # change brody to case, etc
        url = "https://eatatstate.com/menus/case/2015-11-" + str(x+date)
        soup = grabPage(url)
        name = soup.find("div", class_="date-heading").text
        print("The menu for " + str(name))
        grabDaysFood(soup)
        time.sleep(5)

def grabPage(url):
    req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    return BeautifulSoup(html)

def grabMenus(date):
    lst_of_links = []
    url = "https://eatatstate.com/menus"
    soup = grabPage(url)
    content = str(soup.find_all('div',class_="content")[5])
    help = BeautifulSoup(content)
    for link in help.find_all('a'):
       lst_of_links.append(link.get('href'))
    lst_of_links = [x for x in lst_of_links if x!="/menus"]
    for link in lst_of_links:
        if "/menus" in link:
            grabFoodPage(date,link)

def grabDaysFood(soup):
    #grabs all the view-content tags
    viewContent = soup.find_all("div", class_="view-content")[1]
    for tables in viewContent.contents:
        if tables and tables != '\n':
            body = tables.contents[5]
            oddView = [x for x in body.contents if x!='\n']
            menuValue = [a for a in oddView if a!='\n']
            for value in menuValue:
                itemLst = [x for x in value.contents if x != '\n']
                #print(itemLst)
                for item in itemLst:
                    lst = [a for a in item.contents if a != '\n']
                    if lst:
                        for food in lst:
                            if('\n' not in food):
                                if food != " ":
                                    #prints each field items
                                    print(food.text)
            print()
            print()

def main():
    date = int(input("Enter the number of the day"))
    grabFoodPage(date)

main()

