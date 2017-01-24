import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import datetime


cafeNames = ["brody", "shaw"]#,"riverwalk","case","akers", "holmes","hubbard","holden","wilson","landon","gallery"]
day = datetime.date.today().day
month = datetime.date.today().month
print("month: ", month)
print("today is the : ", day)


def soupForCafe():
    for cafe in cafeNames:
        url = "https://eatatstate.com/menus/" + cafe + "/2017-" + str(month) + "-" + str(day)
        req = urllib.request.Request(url, None, headers={'User-Agent' : 'Mozilla/5.0'})
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        addToMeals(soup, cafe)

lunch = {}
breakfast = {}
dinner = {}
latenight = {}
allMeals = {}

def addToMeals(soup,cafe):
    # grabs all the view-content tags, we want the first one
    viewContent = soup.find_all("div", class_="view-content")[1]
    # each dining place is in a table, so lets iterate over those
    for tables in viewContent.contents:
        # if the table isn't empty and isn't a new line character
        if tables and tables != '\n':
            # scraping is weird and inserts new line characters into lists
            # so the body is actually the fifth spot in the array
            body = tables.contents[5]
            # grab oddview and filter out new line character
            oddView = [x for x in body.contents if x!='\n']
            # filter new line character again
            menuValue = [a for a in oddView if a!='\n']
            # now lets grab all the menu values
            for value in menuValue:
                # filter again
                counter = 0
                itemLst = [x for x in value.contents if x != '\n']
                # print("i: ", itemLst);
                # if("lunch" in str(itemLst[1])):
                #     print("yup")
                #     isLunch = True
                print()
                # for every item in the food values
                for item in itemLst:
                    # filter list
                    lst = [a for a in item.contents if a != '\n']
                    if lst:
                        # every food item
                        for food in lst:
                            if('\n' not in food):
                                if food != " ":
                                    # prints each field items
                                    # print(food.text)
                                    if(counter == 0):
                                        breakfast[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "breakfast"]
                                    elif(counter == 1):
                                        lunch[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "lunch"]

                                    elif(counter == 2):
                                        dinner[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "dinner"]

                                    else:
                                        latenight[food.text] = [cafe]


                    counter += 1

            print()
            print()


def whereIsMyFavorite(name):
    print("Your favorite meal is at", allMeals[name][0], "for", allMeals[name][1])


def main():
    soupForCafe()

main()
print()
whereIsMyFavorite("Ham")
# print("breakfast: ", breakfast)
# print("lunch: ", lunch)
# print("dinner: ", dinner)




