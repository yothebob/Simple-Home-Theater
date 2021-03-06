from cli.app import CliApp
# from flask import Flask, render_template, request, g, url_for
# from webapp.forms import LoginForm, CreateUserForm
import core.core_settings as settings
from cli.command_functions import *

app = CliApp()


def show_user_categories(user_categories):
    print("user categories:")
    [print(index,": ",user_categories[index].name) for index in range(len(user_categories))]
    print("type a number to pick a category:\n")




def main_page(user):
    print("""
        type a command in:
    """)
    user_input = input(": ")
    command_dictionary = {
        "add"    : ["add","-a","-add","--add"],
        "sync" : ["sync", "-s", "--sync", "reload", "load", "-r for recursive"],
        "watched": ["watched", "--watched", "-watched" , "-w", "watch", "--watch"],
        "passwd" : ["passwd", "--passwd", "password", "-p", "--password"],
        "exit"   : ["exit", "end", "-e", "--end", "--exit"],
        "help"   : ["help","-h","--help"],
        "category" : ["cat", "category", "-cat", "--category","ls"]
    }
    split_command = user_input.split(" ")

    if user_input.lower() in command_dictionary["help"]:
        print("Commands: ")
        print([print(key,val) for key, val in command_dictionary.items()])
        return main_page(user)

    elif user_input.lower() in command_dictionary["category"]:
        user_categories = user.load_categories()
        show_user_categories(user_categories)
        user_input = input(": ")
        if user_input.isnumeric():
            picked_category = user_categories[int(user_input)]
            user.current_category = picked_category
            print(f"in {user.current_category.name} category...")
            get_command = input(": ")
            run_command = content_commands(user,picked_category,get_command)
        else:
            print("not valid")
            return main_page(user)
        while get_command.lower() != "exit":
            get_command = input(": ")
            # user.create_playlist()
            run_command = content_commands(user,picked_category,get_command)
        return main_page(user)

    elif split_command[0] in command_dictionary["add"]:
        if "-r" in split_command:
            name = input("What is the name of the New Category?: ")
            folder_location = input("What is the path the the folder?: ")
            user.recursive_add_category(name,folder_location)
        else:
            name = input("What is the name of the New Category?: ")
            folder_location = input("What is the path the the folder?: ")
            user.add_category(name,folder_location)
        return main_page(user)

    elif split_command[0] in command_dictionary["sync"]:
        if "-r" in split_command:
            user.recursive_sync_categories()
        else:
            user.sync_categories()
        return main_page(user)

    elif user_input.lower() in command_dictionary["watched"]:
        user.get_watched()
        return main_page(user)

    elif user_input.lower() in command_dictionary["passwd"]:
        user.change_password()
        return main_page(user)

    elif user_input.lower() in command_dictionary["exit"]:
        exit()

    else:
        print("Sorry please try Again")
        return main_page(user)


def run_app():
    user = app.home_page()
    main_page(user)
    print(user.watched)


run_app()
