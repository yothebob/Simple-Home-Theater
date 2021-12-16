#core
from time import sleep

#local
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from cli.app import CliApp


def autoplaying(time_left,start_time=settings.AUTOPLAY_COUNTDOWN):
        if time_left == 0:
            print(time_left)
            return
        elif time_left < (start_time/2):
            print(time_left)
            sleep(1)
            return autoplaying(time_left -1)
        else:
            print(time_left)
            sleep(1)
            return autoplaying(time_left -1)


#for now play_next will go here but it should move to cli.main probably
# i Need to redo this function, it is not working properly and getting the next pk in contents.csv will not work anyways, could be another users or another type of content
def play_next(picked_content,playlist=None):
    # this is just returning the next contents index number
    ''' play the next in a playlist (or just the next in line) given the last picked content'''
    if playlist is None:
        return picked_content + 1



def content_commands(user, category_contents, user_input):

    content_number = ''.join(map(str,[user_input[index] for index in range(len(user_input)) if user_input[index].isnumeric()]))
    print(content_number)
    print('''
        type {content number} {comand} {etc}
        ex: 63 -p   this runs play content #63

        commands:

            play - ["play", "-p"]

            search - ["search", "-s"]

            autoplay - ["-a", "auto" ,"autoplay"]
            autoplay after content is over
    ''')
    split_command = user_input.split(" ")

    command_dictionary = {
    "play"      : ["play", "-p"],
    "details"   : ["checkout", "details", "-v", "-c", '-d'],
    "search"    : ["search", "-s"],
    "autoplay"    : ["-a", "auto" ,"autoplay","-auto"]
    }
    run_command = ""
    for command in split_command:
        if command in command_dictionary["play"]:
            run_command += "play."
        elif command in command_dictionary["details"]:
            run_command += "details."
        elif command in command_dictionary["search"]:
            run_command += "search."
        elif command in command_dictionary["autoplay"]:
            run_command += "autoplay."

    autoplay = False

    if "autoplay" in run_command:
        print("auto play enabled")
        autoplay = True

    if "play" in run_command:
        print("playing")
        picked_content = category_contents.content_list[int(split_command[0])]
        picked_content.play_content()
        play_count = -1
        while autoplay:
            autoplaying(settings.AUTOPLAY_COUNTDOWN)
            play_count += 1 # a crappy ghetto way to do this :(
            next_index = play_next(int(split_command[0]) + play_count)
            picked_content = category_contents.content_list[next_index]
            picked_content.play_content()


    if "details" in run_command:
        split_command = user_input.split(" ")
        print(split_command)
        picked_content = category_contents[int(split_command[0])]
        print(picked_content.name)

    if "search" in run_command:
        picked_category = user.current_category
        command = search_category_contents(picked_category)
        run_command = content_commands(user,picked_category,command)
