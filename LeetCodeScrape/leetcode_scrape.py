

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests
import time
from random import randint
import json
# Importing Twilio so we can text our phone
from twilio.rest import TwilioRestClient

questions_dict = {}
questions_lst = []
filename = "questions.json"

ACCOUNT_SID = "ACed9656eb23b8b6f22bc0070e0bc73f99"
AUTH_TOKEN = "9c683e2d527a4617576fa4000e5c8339"


class Question:
    def __init__(self, title, difficulty):
        self.title = title
        self.description = ""
        self.tags = []
        self.difficulty = difficulty


def textMessage(msg):
    '''
    Twilio function to text our phone
    :param msg: Message we're texting to our phone
    :return:
    '''
    # Find these values at https://twilio.com/user/account
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="(616) 238-3511", from_="(616) 920-6564",
                                 body=msg)

def grab_questions():
    """
    GET Request to grab all the questions name's and difficulty
    :return:
    """
    counter = 1
    # try:
    url = "https://leetcode.com/api/problems/algorithms/"
    headers_dict = {'User-Agent': 'Mozilla/5.0', "Cookie": "__atuvc=4%7C11; csrftoken=io8BL2v2XklVEwRvQWvTnKGkF9eTjEj4VQxdZMZEMwwEiQTWATCwMid9SLIUtPYi; _ga=GA1.2.782661392.1489609798; _gat=1","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, sdch, br"}
    response = requests.get(url, headers=headers_dict)
    sleep_random_time()
    questions = response.json()["stat_status_pairs"]
    print("q: ", questions)
    #questions = open_questions()
    # for all the questions, grab their info
    # for question in questions:
    for question in questions:
        # Only do the questions not behind the pay wall
        if(not question['paid_only']):
            # print("question: ",question)
            title = question['stat']['question__title_slug']
            difficulty = question['difficulty']['level']
            # print("title: ", title)
            questions_dict[title] = Question(title, difficulty)
            counter += 1
    # except Exception as e:
    #     print("error")
    #     textMessage(str("Error on: " + str(counter) + " \n" + "Error msg: " +str(e)))

def open_questions():
    data = []  # List of Record objects

    with open("questions.json") as json_data:
        json_obj = json.load(json_data)
        for d in json_obj:
            data.append(d)
    print("len: ", len(data))
    #return data

def sleep_random_time():
    """
    Sleeps a random amount of time between 3 and 9 seconds
    :return: none
    """
    # get a random number of time to sleep
    sleep_time = randint(3, 9)
    # sleep a random amount of time to prevent getting rate blocked
    #time.sleep(sleep_time)


def grab_problem(question):
    """
    Grabs the questions description and tags
    :param question: Question object passed in by reference so we're directly editing it
    :return: nothing
    """
    try:
        url = "https://leetcode.com/problems/" + question.title
        req = urllib.request.Request(url, None, headers={'User-Agent' : 'Mozilla/5.0'})
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find("div", id="tags")
        if(tags is not None):
            print("tags: ", tags)
            for children in tags.find_next_sibling("span").contents:
                if(children != '\n'):
                    question.tags.append(children.contents[0])
        description = soup.find("meta", {"name": "description"})['content']
        question.description = description
        # print("desc: ", question.description)
        print("tags: ", question.tags)
    except Exception as e:
        textMessage("Error in grab problems ")
        textMessage("Error on: " + question.title + " \n" + "Error msg: " + e)


def write_to_json(filename, data):
    with open(filename, 'w') as outfile:
        # print("data: ", data)
        json.dump(data, outfile)


def build_problems():
    failed = False
    # Loop through the question objects
    for question in questions_dict.values():
        try:
            grab_problem(question)
            print("data: ", question.__dict__)
            print()
            print()
            questions_lst.append(question.__dict__)
            sleep_random_time()
        except Exception as e:
            failed = True
            textMessage("Error in build problems ")
            textMessage("Error on: " + question.title + " \n" + "Error msg: " + e)
    return failed


def main():
    grab_questions()
    did_fail = build_problems()
    if(not did_fail):
        textMessage("Script successfully ran")
    # print("questions list: ", questions_lst)
    # Write the questions to json
    write_to_json(filename, questions_lst)


# main()
open_questions()












