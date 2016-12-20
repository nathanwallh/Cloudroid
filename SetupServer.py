######################
# SetupServer.py
# Setup the FTP server.
######################
"""
OPTIONS:
--------
-delall
    Delete all users.

-del <username1> <username2> ...
    Delete users by username.

-add <username1>:<password1> <username2>:<password2> ...
    Add users.
"""


#!/usr/bin/python3
from shutil import rmtree
from os import path
from UinfoFunc import add_new_username, get_all_usernames_from_file, delete_all_users, delete_user
from argparse import ArgumentParser

FILENAME = 'Uinfo.txt'


def deldirs(dirlist):
    for x in dirlist:
        if path.exists(x):
            rmtree(x)


def argument_parser():
    parser = ArgumentParser(description='Managing users - Delete and Add User.')
    parser.add_argument('-delall', type=str, help="Delete all username in file")
    parser.add_argument('-delete', type=str, help='Deleting the username as enter\r\n'
                                              '<username1>:<username2>')
    parser.add_argument('-add', type=str, help='Add the username as enter\r\n'
                                               '<username1>:<password1> <username2>:<password2>')
    return parser.parse_args()


def main():
    # print(__doc__)
    args = argument_parser()

    if args.add is not None:
        add_new_username(FILENAME, args.add)
    elif args.delall is not None:
        delete_all_users(FILENAME)
    elif args.delete is not None:
        # Get all the users that need to be deleted
        delete_users = args.delete
        # Get all the users that the server
        all_users = get_all_usernames_from_file(FILENAME)

        delete_users = delete_users.split(":")
        for user in delete_users:
            user = user.lower()
            if user in all_users.keys():
                all_users.pop(user, None)

        delete_user(all_users, FILENAME)


if __name__ == "__main__":
    main()
