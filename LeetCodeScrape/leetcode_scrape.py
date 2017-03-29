import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests
import time
from random import randint
import json
# Importing Twilio so we can text our phone
from twilio.rest import TwilioRestClient
import keys

questions_dict = {}
questions_lst = []
filename = "questions.json"


class Question:
    def __init__(self, title, difficulty):
        self.title = title
        self.description = ""
        self.tags = []
        self.difficulty = difficulty


def text_message(msg):
    '''
    Twilio function to text our phone
    :param msg: Message we're texting to our phone
    :return:
    '''
    # Find these values at https://twilio.com/user/account
    account_sid = keys.ACCOUNT_SID
    auth_token = keys.AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="(616) 238-3511", from_="(616) 920-6564",
                                 body=msg)


def grab_questions():
    """
    GET Request to grab all the questions name's and difficulty
    :return:
    """
    counter = 1
    url = "https://leetcode.com/api/problems/algorithms/"
    headers_dict = {'User-Agent': 'Mozilla/5.0', "Cookie": "__atuvc=4%7C11; csrftoken=io8BL2v2XklVEwRvQWvTnKGkF9eTjEj4VQxdZMZEMwwEiQTWATCwMid9SLIUtPYi; _ga=GA1.2.782661392.1489609798; _gat=1","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, sdch, br"}
    response = requests.get(url, headers=headers_dict)
    sleep_random_time()
    questions = response.json()["stat_status_pairs"]
    # questions = open_questions()
    # for all the questions, grab their info
    for question in questions:
        # Only do the questions not behind the pay wall
        if(not question['paid_only']):
            # print("question: ",question)
            title = question['stat']['question__title_slug']
            difficulty = question['difficulty']['level']
            # print("title: ", title)
            questions_dict[title] = Question(title, difficulty)
            counter += 1


def open_questions():
    """
    Opens the questions.json instead of hitting their API everytime
    :return: The list of Question objects
    """
    data = []  # List of Record objects

    with open("questions.json") as json_data:
        json_obj = json.load(json_data)
        for d in json_obj:
            data.append(d)
    return data


def sleep_random_time():
    """
    Sleeps a random amount of time between 3 and 9 seconds
    :return: none
    """
    # get a random number of time to sleep
    sleep_time = randint(3, 9)
    # sleep a random amount of time to prevent getting rate blocked
    time.sleep(sleep_time)


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
        text_message("Error in grab problems ")
        text_message("Error on: " + question.title + " \n" + "Error msg: " + e)


def write_to_json(filename, data):
    """
    Writes the question objects to JSON
    :param filename: file we're writing to
    :param data: List of Question Objects
    :return: none
    """
    with open(filename, 'w') as outfile:
        # print("data: ", data)
        json.dump(data, outfile)


def build_problems():
    """
    Adds the questions tags and description to each question object
    :return: if there was a failure in the script
    """
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
            text_message("Error on: " + question.title + " \n" + "Error msg: " + e)
    return failed


def main():
    grab_questions()
    did_fail = build_problems()
    if(not did_fail):
        text_message("Script successfully ran")
    # print("questions list: ", questions_lst)
    # Write the questions to json
    write_to_json(filename, questions_lst)


main()
#open_questions()













