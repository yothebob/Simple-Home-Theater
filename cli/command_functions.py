#core
from time import sleep

#local
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from cli.app import CliApp


def autoplaying(time_left,start_time=settings.AUTOPLAY_COUNTDOWN):
        if time_left == 0:
            return
        elif time_left < (start_time/2):
            print(time_left)
            sleep(1)
            return autoplaying(time_left -1)
        else:
            sleep(1)
            return autoplaying(time_left -1)


#for now play_next will go here but it should move to cli.main probably
# i Need to redo this function, it is not working properly and getting the next pk in contents.csv will not work anyways, could be another users or another type of content
def play_next(picked_content,playlist=None):
    # this is just returning the next contents index number
    ''' play the next in a playlist (or just the next in line) given the last picked content'''
    if playlist is None:
        return picked_content + 1



def search_category_contents(category):
    user_input = input(": ")
    print("searching...")
    [print(index,": ", category.content_list[index].name) for index in range(len(category.content_list)) if user_input.lower() in category.content_list[index].name.lower()]
    user_input = input(": ")
    return user_input



def content_commands(user, category_contents, user_input):

    content_number = ''.join(map(str,[user_input[index] for index in range(len(user_input)) if user_input[index].isnumeric()]))
    print(content_number)
    split_command = user_input.split(" ")

    command_dictionary = {
    "play"      : ["play", "-p"],
    "details"   : ["checkout", "details", "-v", "-c", '-d'],
    "search"    : ["search", "-s"],
    "autoplay"  : ["-a", "auto" ,"autoplay","-auto"],
    "replay"    : ["-r", "replay", "-re"],
    "help"      : ["-h", "help", "--help"],
    "exit"      : ["exit"]
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
        elif command in command_dictionary["replay"]:
            run_command += "replay."
        elif command in command_dictionary["help"]:
            run_command += "help."

    autoplay = False
    replay = False
    if run_command:
        if "autoplay" in run_command:
            print("auto play enabled")
            autoplay = True

        if "replay" in run_command:
            print("replay enabled")
            replay = True

        if "play" in run_command:
            print("playing")
            picked_content = category_contents.content_list[int(split_command[0])]
            picked_content.play_content()
            user.append_watched(picked_content)
            play_count = -1
            while replay:
                try:
                    autoplaying(settings.AUTOPLAY_COUNTDOWN)
                    picked_content = category_contents.content_list[int(split_command[0])]
                    picked_content.play_content()
                    user.append_watched(picked_content)
                except KeyboardInterrupt:
                    print("replay disabled")
                    replay = False

            while autoplay:
                try:
                    play_count += 1 # a crappy ghetto way to do this :(
                    next_index = play_next(int(split_command[0]) + play_count)
                    print(f"{category_contents.content_list[next_index].name} Next up...")
                    autoplaying(settings.AUTOPLAY_COUNTDOWN)
                    picked_content = category_contents.content_list[next_index]
                    picked_content.play_content()
                    user.append_watched(picked_content)
                except KeyboardInterrupt:
                    print("auto play disabled")
                    autoplay = False


        if "details" in run_command:
            split_command = user_input.split(" ")
            print(split_command)
            picked_content = category_contents[int(split_command[0])]
            print(picked_content.name)

        if "search" in run_command:
            print("searching...")
            picked_category = user.current_category
            command = search_category_contents(picked_category)
            run_command = content_commands(user,picked_category,command)
    else:
        print("please try again")
        return
    return
