#!/usr/bin/python3


__doc__
'''
Methods for dealing with the users file Uinfo.txt
Reads and parses Uinfo.txt. Returns a list of dictionaries: [ {username:xxx,password:yyy} ].
'''


def get_all_usernames_from_file(filename):
    data = ""
    with open(filename, "r") as file1:
        data += file1.read()

    # Removes all empty lines
    data = [line for line in data.split('\n') if line.strip() != '']
    """ The structure of user input looks like this:
     {
         Username
         password
     }
    """
    users_dict = {}
    for i in range(0, data.__len__(), 4):
        if data[i] == "{" and data[i+3] == "}":
            users_dict[data[i+1].lower()] = data[i+2]

    return users_dict


def add_new_username(filename, new_username_info):
    # Get all Username in file
    all_username_dict = get_all_usernames_from_file(filename)

    new_username_info = new_username_info.replace(" ", "")
    new_username_info = new_username_info.replace(",", "")
    new_username_info = new_username_info.replace(";", "")
    new_username_info = new_username_info.split("\n")

    for line in new_username_info:
        username_info = line.split(":")
        if username_info.__len__() == 2:
            key = username_info[0].lower()
            password = username_info[1]
            if key not in all_username_dict.keys():
                all_username_dict[key] = password

    with open(filename, 'w') as file:
        for key, value in all_username_dict.items():
            file.write("{\n")
            file.write(key + "\n")
            file.write(value + "\n")
            file.write("}\n\n")


def delete_all_users(filename):
    open(filename, 'w')


def delete_user(all_username_dict, filename):
    with open(filename, 'w') as file:
        for key, value in all_username_dict.items():
            file.write("{\n")
            file.write(key + "\n")
            file.write(value + "\n")
            file.write("}\n\n")



