"""
CSE 480: Project 1
Created by Josh Benner, 1/24/17
"""

import json, csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


class Node:
    """
    Not used.. useful if there were nested levels of tags/objects/csv lines
    """
    def __init__(self, tag, data):
        self.tag = tag
        self.data = data


class Record:
    """
    Class record that holds all record data items after the initial tag/obj/line
    """
    def __init__(self, data):
        self.data = data  # Dictionary that holds the data for the 2d tag/obj/lines

    def add_node(self, data):
        """
        Also not used, but would be useful if more than 2 deep nested levels
        :param data:
        :return:
        """
        for attribute, value in data.items():
            node = Node(attribute, value)
            self.data.append(node)


def read_csv_file(filename):
    """
    Takes a filename denoting a CSV formatted file.
    Returns an object containing the data from the file.
    The specific representation of the object is up to you.
    The data object will be passed to the write_*_files functions.
    """
    data = []  # List of Record objects

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(Record(row))

    return data


def write_csv_file(filename, data):
    """
    Takes a filename (to be writen to) and a data object
    (created by one of the read_*_file functions).
    Writes the data in the CSV format.
    :param filename: The file name to write to
    :param data: A record Object
    :return:
    """
    with open(filename, "w") as outfile:
        fieldnames = data[0].data.keys()
        csvwriter = csv.DictWriter(outfile, sorted(fieldnames))
        data_obj = []
        for d in data:
            data_obj.append(d.data)
        csvwriter.writeheader()
        csvwriter.writerows(data_obj)

def write_emails_to_csv(filename, data, field="EmailAddress"):
    data_dict = {field: "1"}
    data_obj = []
    for d in data:
        data_obj.append({"EmailAddress": d})
    print("d_obj: ", data_obj)
    with open(filename, "w") as outfile:
        fieldnames = data_dict.keys()
        csvwriter = csv.DictWriter(outfile, sorted(fieldnames))
        csvwriter.writeheader()
        csvwriter.writerows(data_obj)

def read_json_file(filename):
    """
    Similar to read_csv_file, except works for JSON files.
    List of objects, each with X number of properties
    """
    data = []  # List of Record objects

    with open(filename) as json_data:
        json_obj = json.load(json_data)
        for d in json_obj:
            data.append(Record(d))
    return data


def write_json_file(filename, data):
    """
    Writes JSON files. Similar to write_csv_file.
    :param filename: file path we give it
    :param data: our common data format we created, in this case a Record instance
    :return: none, writes file
    """
    with open(filename, 'w') as outfile:
        data_obj = []
        for d in data:
            data_obj.append(d.data)
        json.dump(data_obj, outfile, sort_keys=True)


def read_xml_file(filename):
    """
    Reads XML file and parses into common data format
    :param filename:
    :return: common data format, list of Record() Instances
    """
    data = []

    tree = ET.parse(filename)
    root = tree.getroot()

    for child in root:
        children_dict = {}
        for children in child:
            children_dict[children.tag] = children.text
        data.append(Record(children_dict))
    return data


def write_xml_file(filename, data):
    """
    Feel free to write what you want here.
    """
    tree = ET.ElementTree()
    element = ET.Element("data")
    tree._setroot(element)
    root = tree.getroot()
    for d in data:
        child = Element("record")
        root.append(child)
        children_list = []
        for key, val in d.data.items():
            children = [key, val]
            children_list.append(children)
        children_list.sort()
        for c in children_list:
            children = Element(c[0])
            children.text = str(c[1])
            child.append(children)

    tree.write(filename)


def compare_user_emails(signed_up_users, full_class_users, key1="emailAddress", key2="preferredEmail"):
    """
    Expects two json data objects and a key and returns everything that is in the data1 but not in data2 - left join)
    :param signed_up_users: list of user objects
    :param full_class_users: list of users with only an email parameter
    :return: list of emails that are in the second list
    """
    print("d2: ", full_class_users)

    list_of_differences = []
    for x in full_class_users:
        if(x not in signed_up_users):
            list_of_differences.append(x)

    # for x in signed_up_users['users']:
    #     if x[key1] not in full_class_users and x[key2] not in full_class_users:
    #         list_of_differences.append(x[key1])
    return list_of_differences


def convert_records_to_dict(recordLst):
    records = []
    for rec in recordLst:
        for val in rec.data.values():
            records.append(val)
    return records

def convert_users_to_lst(signed_up_users):
    list_of_users = []
    for x in signed_up_users['users']:
        list_of_users.append(x["emailAddress"])
    return list_of_users


