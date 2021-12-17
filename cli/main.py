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
    user_input = input(": ")
    return user_categories[int(user_input)]


# currently obsolete
# def show_category_contents(category):
#     "This will just show all contents for now"
#     category_contents = category.content_list
#     [print(index, ": ", category_contents[index].name) for index in range(len(category_contents))] ## TODO: for some reason this is printing too many, but the length is fine?
#     user_input = input(": ")
#     return user_input



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
        print(f"in {picked_category.name} category...")
        get_command = input(": ")
        # user.create_playlist()
        run_command = content_commands(user,picked_category,get_command)
        while get_command.lower() != "exit":
            get_command = input(": ")
            # user.create_playlist()
            run_command = content_commands(user,picked_category,get_command)
        return main_page(user)

    elif user_input.lower() in command_dictionary["add"]:
         user.add_category()
         return main_page(user)

    elif user_input.lower() in command_dictionary["reload"]:
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
