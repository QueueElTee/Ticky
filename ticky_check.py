#!/usr/bin/env python3

import re
import operator
import csv

error = {}
error_list = []
per_user_info = {}
per_user_error = {}
per_user_list = []

def generate_err_dict():
    file = open("syslogp.log", "r")
    pattern = r"ticky: ERROR ([\w ]*) "

    for line in file.readlines():
        if re.search(pattern, line) != None:
            result = re.search(pattern, line)
            error_message = result.group(1)

            if error_message not in error.keys():
                error[error_message] = 0
            error[error_message] += 1
            error_tuple = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
            final_error = dict(error_tuple)

    file.close()
    error.clear()
    error.update(final_error)


def structure_err():
    for err, count in zip(error.keys(), error.values()):
        error_dict = {}
        error_dict["Error"] = err
        error_dict["Count"] = count
        error_list.append(error_dict)


def generate_err_csv():
    error_info = ['Error', 'Count']
    with open('error_message.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=error_info)
        writer.writeheader()
        writer.writerows(error_list)
            


generate_err_dict()
structure_err()
generate_err_csv()




def generate_stats_dict():
    file = open("syslogp.log", "r")
    error_pattern = r"ticky: ERROR ([\w ]*) "
    info_pattern = r"ticky: INFO ([\w ]*) "
    username_pattern = r"\((\w*)\)"
    per_user_error_temp = {}
    per_user_info_temp = {}


    for line in file.readlines():
        if re.search(username_pattern, line) != None:
            user_result = re.search(username_pattern, line).group(1)
            if re.search(error_pattern, line) != None:
                if user_result not in per_user_error_temp.keys():
                    per_user_error_temp[user_result] = 0
                per_user_error_temp[user_result] += 1
            if re.search(info_pattern, line) != None:
                if user_result not in per_user_info_temp.keys():
                    per_user_info_temp[user_result] = 0
                per_user_info_temp[user_result] += 1
    
    file.close()

    per_user_info.update(dict(sorted(per_user_info_temp.items())))
    per_user_error.update(dict(sorted(per_user_error_temp.items())))


def structure_stats():
    for user, error, info in zip(per_user_info.keys(), per_user_error.values(), per_user_info.values()):
        per_user = {}
        per_user["Username"] = user
        per_user["INFO"] = info
        per_user["ERROR"] = error
        per_user_list.append(per_user)


def generate_stats_csv():
    stats_info = ['Username', 'INFO', 'ERROR']
    with open('user_statistics.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=stats_info)
        writer.writeheader()
        writer.writerows(per_user_list)



generate_stats_dict()
structure_stats()
generate_stats_csv()