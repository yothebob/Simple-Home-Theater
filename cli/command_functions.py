#core
from time import sleep
from random import choice, randrange

#local
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from cli.app import CliApp
from movie_scraper.main import find_metadata

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

def play_random(content_list,playlist=None):
    if playlist is None:
        return choice(content_list)
    # else:
    #     return randrange(len(content_list))

def search_category_contents(category,user_input=""):
    if user_input == "":
        user_input = input(": ")
    print(f"searching {user_input}...")
    [print(index,": ", category.content_list[index].name) for index in range(len(category.content_list)) if user_input.lower() in category.content_list[index].name.lower()]



def content_commands(user, category_contents, user_input):

    content_number = ''.join(map(str,[user_input[index] for index in range(len(user_input)) if user_input[index].isnumeric()]))
    print(content_number)
    split_command = user_input.split(" ")
    print(f"In {category_contents.name} category...")
    command_dictionary = {
    "play"      : ["play", "-p"],
    "list"      : ["ls", "(-d for double list)"],
    "details"   : ["checkout", "details", 'det'],
    "search"    : ["search", "-s"],
    "autoplay"  : ["-a", "auto" ,"autoplay","-auto"],
    "replay"    : ["-r", "replay", "-re"],
    "shuffle": ["-sp","shuffle", "-shuffle", "-randomize"],
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
        elif command in command_dictionary["list"]:
            run_command += "list."
        elif command in command_dictionary["shuffle"]:
            run_command += "shuffle."

    autoplay = False
    replay = False
    shuffle = False

    if run_command:
        if "autoplay" in run_command:
            print("auto play enabled")
            autoplay = True

        if "replay" in run_command:
            print("replay enabled")
            replay = True

        if "shuffle" in run_command:
            print("shuffle enabled")
            shuffle = True

        if "play" in run_command:
            print("playing")
            if split_command[0].isnumeric():
                content_indexes = [index for index in split_command if index.isnumeric()]
                print(content_indexes)
                play_count = -1
                for content_index in content_indexes:
                    picked_content = category_contents.content_list[int(content_index)]
                    picked_content.play_content()
                    user.append_watched(picked_content)
            else:
                print("no index given... please try again")
            while replay:
                try:
                    content_indexes = [index for index in split_command if index.isnumeric()]
                    for content_index in content_indexes:
                        autoplaying(settings.AUTOPLAY_COUNTDOWN)
                        picked_content = category_contents.content_list[int(content_index)]
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

            while shuffle:
                try:
                    content_indexes = [index for index in split_command if index.isnumeric()]
                    if len(content_indexes) > 1:
                        picked_index = play_random(content_indexes)
                        picked_content = category_contents.content_list[int(picked_index)]
                    else:
                        picked_content = play_random(category_contents.content_list)
                    print(f"{picked_content.name} Next up...")
                    autoplaying(settings.AUTOPLAY_COUNTDOWN)
                    picked_content.play_content()
                    user.append_watched(picked_content)
                except KeyboardInterrupt:
                    print("shuffle disabled")
                    shuffle = False


        if "details" in run_command:
            split_command = user_input.split(" ")
            print(split_command)
            if len(split_command) > 2: # default command needs 2 args. $ {number} details
                for content_index in range(len(split_command)):
                    if content_index != len(split_command)-1:
                        content_data = find_metadata(category_contents.content_list[int(split_command[int(content_index)])].name)
                        [print(settings.METADATA_LIST[index],": ",content_data[index][0],"\n") for index in range(len(settings.METADATA_LIST))]
            # old [print(category_contents.content_list[int(split_command[index])].name,"\n",find_metadata(category_contents.content_list[int(split_command[index])].name)) for index in range(len(split_command)) if index != (len(split_command)-1)]
            else:
                picked_content = category_contents.content_list[int(split_command[0])]
                print(picked_content.name)
                content_data = find_metadata(picked_content.name)
                [print(settings.METADATA_LIST[index], ": ", content_data[index][0]) for index in range(len(content_data))]

        if "search" in run_command:
            print(split_command)
            if len(split_command) > 1:
                picked_category = user.current_category
                [search_category_contents(picked_category,index) for index in split_command if index != "-s"]
            else:
                picked_category = user.current_category
                search_category_contents(picked_category)

        if "list" in run_command:
            if "-d" in split_command:
                #print 2 contents per line
                [print(index-1," : ",user.current_category.content_list[index-1].name, "\t\t",index," : ",user.current_category.content_list[index].name) for index in range(len(user.current_category.content_list)) if index%2 == 0]
            else:
                [print(index," : ",user.current_category.content_list[index].name) for index in range(len(user.current_category.content_list))]
        if "help" in run_command:
            print("Commands:\n")
            [print(key, item) for key, item in command_dictionary.items()]
    else:
        print("please try again")
        return
    return
