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
            print(time_left)
            sleep(1)
            return autoplaying(time_left -1)


#for now play_next will go here but it should move to cli.main probably


def play_list(user,obj_content_list=[],playstyle=[],play_countdown=3):
    #a new generic function that will take care of playing a list of content OBJECTS
    # and handle shuffle, replay, autoplay and play accordingly

    if "shuffle" in playstyle:
        #randomize the list
        randomized_content_list = []
        for number in range(len(obj_content_list)):
            random_obj = choice(obj_content_list)
            obj_content_list.remove(random_obj)
            randomized_content_list.append(random_obj)
        obj_content_list = randomized_content_list

        for obj_content in obj_content_list:
            #keep replaying
            autoplaying(play_countdown)
            obj_content.play_content()
            user.append_watched(obj_content)
        return

# for obj_content in obj_content_list:
    if "replay" in playstyle:
            for obj_content in obj_content_list:
                #keep replaying
                autoplaying(play_countdown)
                obj_content.play_content()
                user.append_watched(obj_content)
            return

    elif "autoplay" in playstyle:
        #after playing list, play the whole category (try to start from last used index)

        #play list
        for index_num in obj_content_list: # number not objects here!
            autoplaying(play_countdown)
            user.current_category.content_list[index_num].play_content()
            user.append_watched(user.current_category.content_list[index_num])

        remainder_index = obj_content_list[-1] + 1

        # play remainder of category
        while remainder_index < len(user.current_category.content_list):
            autoplaying(play_countdown)
            user.current_category.content_list[remainder_index].play_content()
            user.append_watched(user.current_category.content_list[remainder_index])
            remainder_index += 1
        return
    else:
        #play the list then return
        for obj_content in obj_content_list:
            print(obj_content)
            autoplaying(play_countdown)
            obj_content.play_content()
            user.append_watched(obj_content)
        return


def search_category_contents(category,user_input=""):
    if user_input == "":
        user_input = input(": ")
    print(f"searching {user_input}...")
    [print(index,": ", category.content_list[index].name) for index in range(len(category.content_list)) if user_input.lower() in category.content_list[index].name.lower()]



def content_commands(user, category_contents, user_input):

    content_number = ''.join(map(str,[user_input[index] for index in range(len(user_input)) if user_input[index].isnumeric()]))
    split_command = user_input.split(" ")
    print(f"In {category_contents.name} category...")
    command_dictionary = {
    "play"      : ["play", "-p", "countdown=?"],
    "list"      : ["ls", "(-d for double list)", "ls {start} {stop} "],
    "detail"   : ["checkout", "details", 'det'],
    "list playlist" : ["-lpl","listpl"],
    "add playlist" : ["{indexes} -apl name=?","-apl","addl"],
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
        elif command in command_dictionary["detail"]:
            run_command += "detail."
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
        elif command in command_dictionary["list playlist"]:
            run_command += "listplaylist."
        elif command in command_dictionary["add playlist"]:
            run_command += "addplaylist."

    autoplay = False
    replay = False
    shuffle = False
    been_played = False

    if run_command:
        if "autoplay." in run_command:
            print("auto play enabled")
            autoplay = True

        if "replay." in run_command:
            print("replay enabled")
            replay = True

        if "shuffle." in run_command:
            print("shuffle enabled")
            shuffle = True

        if "play." in run_command:
            print("playing")
            play_countdown = settings.AUTOPLAY_COUNTDOWN # we set this here do it can be temp changed from a command

            for command in split_command:
                #change countdown number
                if "countdown" in command:
                    arg = [command for command in split_command if "countdown" in command][0]
                    countdown = [char for char in arg if char.isnumeric()]
                    print('new countdown',"".join(countdown))
                    play_countdown = int("".join(countdown))

            content_pl = None
            
            #get playlist
            if split_command[0] in [pl.name for pl in user.current_category.playlist_lists]:
                selected_pl = [pl for pl in user.current_category.playlist_lists if pl.name==split_command[0]][0]
                content_pl = selected_pl.content_list
                print(content_pl)


            while replay:
                try:
                    if content_pl is None:
                        content_pl = [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["replay"],play_countdown)
                    been_played = True
                except KeyboardInterrupt:
                    print("replay disabled")
                    replay = False
                    been_played = True

            while autoplay:
                try:
                    #warning: autoplay does not currently work with playlists, it takes a list of index not objects
                    content_pl = [int(index) for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["autoplay"],play_countdown)
                    autoplay = False
                    been_played = True
                except KeyboardInterrupt:
                    print("auto play disabled")
                    autoplay = False
                    been_played = True

            while shuffle:
                try:
                    if content_pl is None:
                        content_pl = [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["shuffle"],play_countdown)
                    shuffle = False
                    been_played = True
                except KeyboardInterrupt:
                    print("shuffle disabled")
                    shuffle = False
                    been_played = True
            if been_played == False:
                if content_pl is None:
                    content_pl = [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
                play_list(user,content_pl,[],play_countdown)


        if "detail." in run_command:
            split_command = user_input.split(" ")
            print(split_command)
            if len(split_command) > 2: # default command needs 2 args. $ {number} details
                for content_index in range(len(split_command)):
                    if content_index != len(split_command)-1:
                        content_data = find_metadata(category_contents.content_list[int(split_command[int(content_index)])].name)
                        [print(settings.METADATA_LIST[index],": ",content_data[index][0],"\n") for index in range(len(settings.METADATA_LIST))]
            else:
                picked_content = category_contents.content_list[int(split_command[0])]
                print(picked_content.name)
                content_data = find_metadata(picked_content.name)
                [print(settings.METADATA_LIST[index], ": ", content_data[index][0]) for index in range(len(content_data))]

        if "search." in run_command:
            print(split_command)
            if len(split_command) > 1:
                picked_category = user.current_category
                [search_category_contents(picked_category,index) for index in split_command if index != "-s"]
            else:
                picked_category = user.current_category
                search_category_contents(picked_category)

        if "list." in run_command:
            if len(split_command) > 2:
                list_range = [int(num) for num in split_command if num.isnumeric()]
                print(list_range)
                if len(list_range) == 2:
                    [print(index," : ",user.current_category.content_list[index].name) for index in range(len(user.current_category.content_list)) if index >= list_range[0] and index <= list_range[-1]]
            elif "-d" in split_command:
                #print 2 contents per line
                [print(index-1," : ",user.current_category.content_list[index-1].name, "\t\t",index," : ",user.current_category.content_list[index].name) for index in range(len(user.current_category.content_list)) if index%2 == 0]
            else:
                [print(index," : ",user.current_category.content_list[index].name) for index in range(len(user.current_category.content_list))]
        if "help." in run_command:
            print("Commands:\n")
            [print(key, item) for key, item in command_dictionary.items()]

        if "addplaylist." in run_command:
            list_range = [user.current_category.content_list[int(num)].pk for num in split_command if num.isnumeric()]
            print(list_range)
            playlist_name = str(split_command[-1].replace("name=",""))
            user.create_playlist(playlist_name,list_range)

        if "listplaylist." in run_command:
            [print(index.name,"\n",[con.name for con in index.content_list]) for index in user.current_category.playlist_lists]
    else:
        print("please try again")
        return
    return
