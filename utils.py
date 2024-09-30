from lxml import objectify
import os
import glob
import json


def fetch_labels_mapping():
    with open("labels_mapping.txt") as file:
        entry = [line.split("=") for line in file.readlines()]
    return {key.strip(): value.strip() for key, value in entry}


def fetch_allowed_labels():
    with open("allowed_labels.txt") as file:
        return [line.strip('\n') for line in file.readlines()]


def _map_label(label, labels_mapping):
    if label in labels_mapping:
        return labels_mapping[label]
    else:
        return label


def _is_label_approved(label, approved_labels):
    return label in approved_labels


def convert_label(label, labels_mappings, approved_labels):
    mapped_label = _map_label(label, labels_mappings)

    if _is_label_approved(mapped_label, approved_labels):
        return mapped_label
    return None


def read_xml_file(file_path):
    with open(file_path) as file:
        return objectify.fromstring(file.read())


def read_xml_files(file_path):
    files = list()
    for file_name in file_path.split(';'):
        if os.path.isdir(file_name):
            xml_files = glob.glob(file_name + '/*.xml')
            for file in xml_files:
                files.append(read_xml_file(file))
        else:
            files.append(read_xml_file(file_name))

    return files

def extract_comment_authors(file):
    file_name = 'jira_users.json'
    try:
        with open(file_name, 'r') as json_file:
            authors = json.load(json_file)
    except FileNotFoundError:
        print("json_users.json not found")
        authors = {}

    for item in file.channel.item:
        authors[str(item.reporter.get('accountid'))] = str(item.reporter) 
        authors[str(item.assignee.get('accountid'))] = str(item.assignee)
    
    with open(file_name, 'w') as json_file:
        json.dump(authors, json_file, indent=4)
        
    return authors
    
    