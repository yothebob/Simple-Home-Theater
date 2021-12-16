from cli.app import CliApp
# from flask import Flask, render_template, request, g, url_for
# from webapp.forms import LoginForm, CreateUserForm
import core.core_settings as settings
from cli.command_functions import *

app = CliApp()


def home_page():
    '''welcome screen function and login/create user functionality'''
    print("""
        {}

        type 'login' to login as existing user.
        type 'create' to create new user.
        """.format(settings.APP_NAME))
    user_input = input(": ")
    if user_input.lower() == "login":
        return app.login()
    elif user_input.lower() == "create":
        app.create_user()
        return app.login()


def show_user_categories(user_categories):
    print("user categories:")
    [print(index,": ",user_categories[index].name) for index in range(len(user_categories))]
    print("type a number to pick a category:\n")
    user_input = input(": ")
    return user_categories[int(user_input)]



def show_category_contents(category):
    "This will just show all contents for now"
    print("""Category contents:
            type the number, then type ...
            play - play contents
            checkout - see content metadata
    """)
    category_contents = category.content_list
    [print(index, ": ", category_contents[index].name) for index in range(len(category_contents))] ## TODO: for some reason this is printing too many, but the length is fine?
    user_input = input(": ")
    return user_input



def search_category_contents(category):
    user_input = input(": ")
    print("searching...")
    # results_list = [ content for content in category.content_list if user_input.lower() in content.name.lower()]
    [print(index,": ", category.content_list[index].name) for index in range(len(category.content_list)) if user_input.lower() in category.content_list[index].name.lower()]
    user_input = input(": ")
    return user_input

            #show content details/metadata



def main_page(user):
    print("""
        type a command in:
    """)
    user_input = input(": ")
    command_dictionary = {
        "add"    : ["add","-a","-add","--add"],
        "reload" : ["reload", "-r", "--reload", "-reload", "re", "-re", "load"],
        "watched": ["watched", "--watched", "-watched" , "-w", "watch", "--watch"],
        "passwd" : ["passwd", "--passwd", "password", "-p", "--password"],
        "exit"   : ["exit", "end", "-e", "--end", "--exit"],
        "help"   : ["help","-h","--help"],
        "category" : ["cat", "category", "-cat", "--category"]
    }
    if user_input.lower() in command_dictionary["help"]:
        print("""
        commands:
    category {}
                - go to your categories list

    add      {}
                - add new category

    reload   {}
                - reload category

    watched  {}
                - show list of played content

    passwd   {}
                - change password

    exit     {}
                - exit program
        """.format(command_dictionary["category"],command_dictionary["add"],command_dictionary["reload"],
        command_dictionary["watched"],command_dictionary["passwd"],command_dictionary["exit"]))
        return main_page(user)

    elif user_input.lower() in command_dictionary["category"]:
        user_categories = user.load_categories()
        picked_category = show_user_categories(user_categories)
        user.current_category = picked_category
        get_command = show_category_contents(picked_category)
        run_command = content_commands(user,picked_category,get_command)
        while get_command.lower() != "exit":
            get_command = show_category_contents(picked_category)
            run_command = content_commands(user,picked_category,get_command)
        return main_page(user)

    elif user_input.lower() in command_dictionary["add"]:
         user.add_category()
         return main_page(user)
    elif user_input.lower() in command_dictionary["reload"]:
        #return user. # this needs to reload the category contents and rename and items and etc, erase any that have been removed, add any new items
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
    user = home_page()
    main_page(user)
    print(user.watched)


run_app()
