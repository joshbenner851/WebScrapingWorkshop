import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import datetime
import keys
import time
from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect, render_template, url_for, make_response
import twilio.twiml
import json

app = Flask(__name__)

import datetime
print(datetime.date.day)

client = TwilioRestClient(keys.ACCOUNT_SID, keys.AUTH_TOKEN)

#cafeNames = ["brody", "shaw","riverwalk","case","akers", "holmes","hubbard","holden","wilson","landon","gallery"]
cafeNames = ["brody","shaw","case","landon"]
day = datetime.date.today().day
month = datetime.date.today().month
dateRange = 7
favoriteFoods = []
days = {}


lunch = {}
breakfast = {}
dinner = {}
latenight = {}
allMeals = {}

def soupForCafe():
    for cafe in cafeNames:
        print("Processing: ", cafe , "...")
        for date in range(0,1):
            url = "https://eatatstate.com/menus/" + cafe + "/2016-" + str(month) + "-" + str(day - date)
            req = urllib.request.Request(url, None,headers={'User-Agent' : 'Mozilla/5.0'})
            time.sleep(3)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html)
            addToMeals(soup,cafe, day-date)

def addToMeals(soup,cafe, day):
    #grabs all the view-content tags, we want the first one
    viewContent = soup.find_all("div", class_="view-content")[1]
    #each dining place is in a table, so lets iterate over those
    for tables in viewContent.contents:
        #if the table isn't empty and isn't a new line character
        if tables and tables != '\n':
            #scraping is weird and inserts new line characters into lists
            #so the body is actually the fifth spot in the array
            body = tables.contents[5]
            #grab oddview and filter out new line character
            oddView = [x for x in body.contents if x!='\n']
            #filter new line character again
            menuValue = [a for a in oddView if a!='\n']
            #now lets grab all the menu values
            for value in menuValue:
                #filter again
                counter = 0
                itemLst = [x for x in value.contents if x != '\n']

                # #print("i: " ,itemLst);
                # if("lunch" in str(itemLst[1])):
                #     print("yup")
                #     isLunch = True
                # #print()

                #for every item in the food values
                for item in itemLst:
                    #filter list
                    lst = [a for a in item.contents if a != '\n']
                    if lst:
                        #every food item
                        for food in lst:
                            if('\n' not in food):
                                if food != " ":
                                    #prints each field items
                                    #print(food.text)
                                    if(counter == 0):
                                        breakfast[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "breakfast", day]
                                        days[(day,food.text)] = [cafe, "breakfast", day]
                                    elif(counter == 1):
                                        lunch[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "lunch", day]
                                        days[(day,food.text)] = [cafe, "lunch", day]
                                    elif(counter == 2):
                                        dinner[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "dinner", day]
                                        days[(day,food.text)] = [cafe, "dinner", day]
                                    else:
                                        latenight[food.text] = [cafe]
                                        allMeals[food.text] = [cafe, "latenight", day]



                    counter += 1

def whereIsMyFavorite(name):
    message = client.messages.create(
        to="6162383511",
        from_="(616) 920-6564",
        body="Your favorite meal," + name + " is at " + allMeals[name][0] + " for " + allMeals[name][1] + " on the " + str(allMeals[name][2])
    )

    print(message.sid)

def favMealsToday(favMeals, day):
    cafes = [[],[],[]]
    for meal in favMeals:
        if( (day,meal) in days):
            food = days[(day, meal)]
            time = food[1]
            food.append(meal)
            if(time == "breakfast"):
                cafes[0].append(food)
            elif(time == "lunch"):
                cafes[1].append(food)
            elif(time == "dinner"):
                cafes[2].append(food)
    print(cafes)
    message = formatMeals(cafes)
    msg = client.messages.create(
        to="6162383511",
        from_="(616) 920-6564",
        body=message
    )
    return message

def formatMeals(cafes):
    msg = ""
    msg += "Your favorite meals for breakfast are: "
    for x in cafes[0]:
        msg += x[0] + " for " + x[3] + " "
    msg += ". \n\nYour favorite meals for lunch are: "
    for x in cafes[1]:
        msg += "\n" + x[0] + " for " + x[3] + " "
    print()
    msg += ". \n\nYour favorite meals for dinner are: "
    for x in cafes[1]:
        msg += "\n" + x[0] + " for " + x[3] + " "
    print()
    return msg

def main():
    soupForCafe()
    #print("Everything: ", allMeals)

@app.route('/')
def index():
    data = get_saved_data()
    return render_template('index.html', saves=data)

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('meals'))
    except TypeError:
        data = {}
    return data

@app.route('/user', methods=['POST'])
def user():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey ")
    response = make_response(redirect(url_for('index')))

    data = get_saved_data()
    data.update(request.form.items())
    msg = favMealsToday(data, day)
    response.set_cookie('meals', json.dumps(data))
    response.set_cookie('places', json.dumps(msg))
    return response


if __name__ == "__main__":
    app.run(debug=True,port=8000)

main()
print()

print()
favMeals = ["-Chicken Shwarma", "Cilantro Lime Rice", "Daeji Bulgogi (Spicy Pork)",
            "-Herb Rice Pilaf", "Michigan Caramel Apple Pork Chops", "Cinnamon Swirl French Toast", "Made to Order Waffles"]

def grabFavMeals():
    str1 = "yes"
    while(str1!="quit"):
        str1 = input("Please enter a favorite meal or 'quit' to quit")
        if(str1 == "fav"):
            whereIsMyFavorite(input("Please enter 1 fav meal"))
        favMeals.append(str1)
    favMealsToday(favMeals, 6)

print(days)
print()
favMealsToday(favMeals, 6)
grabFavMeals()
#print("lunch: ", lunch)
#print("dinner: ", dinner)


