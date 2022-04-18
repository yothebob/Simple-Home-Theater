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
        copied_list = obj_content_list.copy()
        for number in range(len(copied_list)):
            random_obj = choice(copied_list)
            copied_list.remove(random_obj)
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
    print("content results...")
    [print(index,": ", category.content_list[index].name) for index in range(len(category.content_list)) if user_input.lower() in category.content_list[index].name.lower()]
    print("playlists results...")
    [print(category.playlist_lists[index].name,[item.name for item in category.playlist_lists[index].content_list]) for index in range(len(category.playlist_lists)) if user_input.lower() in category.playlist_lists[index].name.lower()]



def content_commands(user, category_contents, user_input):

    content_number = ''.join(map(str,[user_input[index] for index in range(len(user_input)) if user_input[index].isnumeric()]))
    split_command = user_input.split(" ")
    print(f"In {category_contents.name} category...")
    command_dictionary = {
    "play"      : {"play" : "play content", "-p" : "", "countdown=?" : "override countdown between content"},
    "list"      : {"ls" : "list category", "ls {start} {stop}" : "list indexes in a range"},
    "detail"   : {"details" : "show imdb content data"},
    "list playlist" : {"-lpl" : "List playlist","listpl" : ""},
    "add playlist" : {"-apl" : " add playlist ex:{indexes} -apl name=?"},
    "append playlist" : {"-atpl" : " add to a playlist ex:{indexes} -atpl name=?"},
    "search"    : {"search" :"search for multiple names", "-s": ""},
    "autoplay"  : {"-a" : "autoplay category in index order"},
    "replay"    : {"-r": "replay given indexes/ playlist"},
    "shuffle"   : {"-sp" : "shuffle playlist"},
    "cross_content"   : {"-crossc" : "grab a piece of content from another category ex:{-crossc id=(content_id)}"},
    "help"      : {"-h" : "", "help" : ""},
    "exit"      : {"exit" : ""}
    }

    run_command = ""
    for command in split_command:
        if command in command_dictionary["play"].keys():
            run_command += "play."
        elif command in command_dictionary["detail"].keys():
            run_command += "detail."
        elif command in command_dictionary["search"].keys():
            run_command += "search."
        elif command in command_dictionary["autoplay"].keys():
            run_command += "autoplay."
        elif command in command_dictionary["replay"].keys():
            run_command += "replay."
        elif command in command_dictionary["help"].keys():
            run_command += "help."
        elif command in command_dictionary["list"].keys():
            run_command += "list."
        elif command in command_dictionary["shuffle"].keys():
            run_command += "shuffle."
        elif command in command_dictionary["list playlist"].keys():
            run_command += "listplaylist."
        elif command in command_dictionary["add playlist"].keys():
            run_command += "addplaylist."
        elif command in command_dictionary["append playlist"].keys():
            run_command += "appendplaylist."
        elif command in command_dictionary["cross_content"].keys():
            run_command += "cross_content."

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

            content_pl = []
            selected_pl = ""

            if "cross_content." in run_command:
                    print("added cross content")
                    # if commanded add forign content to content_pl
                    content_id = str(split_command[-1].replace("id=",""))
                    foreign_content = query(settings.CONTENT_TABLE,content_id,"pk")
                    if foreign_content:
                        foreign_cat = [cats for cats in user.categories if cats.pk == foreign_content[1]]
                        if foreign_cat:
                            print("appending")
                            content_pl.append(user.current_category.load_content(foreign_content,parent_cat=foreign_cat[0]))
                
            for command in split_command:
                #change countdown number
                if "countdown" in command:
                    arg = [command for command in split_command if "countdown" in command][0]
                    countdown = [char for char in arg if char.isnumeric()]
                    print('new countdown',"".join(countdown))
                    play_countdown = int("".join(countdown))
                #get playlist
                if command in [pl.name for pl in user.current_category.playlist_lists]:
                    selected_pl = [pl for pl in user.current_category.playlist_lists if pl.name==command][0]
                    content_pl += selected_pl.content_list
                    # print(content_pl)             
       
            while replay:
                try:
                    if len(content_pl) == 0:
                        content_pl += [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["replay"],play_countdown)
                    been_played = True
                except KeyboardInterrupt:
                    print("replay disabled")
                    replay = False
                    been_played = True

            while autoplay:
                try:
                    #warning: autoplay does not currently work with playlists, it takes a list of index not objects
                    content_pl += [int(index) for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["autoplay"],play_countdown)
                    autoplay = False
                    been_played = True
                except KeyboardInterrupt:
                    print("auto play disabled")
                    autoplay = False
                    been_played = True

            while shuffle:
                try:
                    if len(content_pl) == 0:
                        content_pl += [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
                    play_list(user,content_pl,["shuffle"],play_countdown)
                    shuffle = False
                    been_played = True
                except KeyboardInterrupt:
                    print("shuffle disabled")
                    shuffle = False
                    been_played = True
            # normal play
            if been_played == False:
                if len(content_pl) == 0:
                    content_pl += [user.current_category.content_list[int(index)] for index in split_command if index.isnumeric()]
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
            [print(key, "\n\t",[f"{k} : {v}" for k,v in item.items() ]) for key, item in command_dictionary.items()]

        if "addplaylist." in run_command:
            list_range = [user.current_category.content_list[int(num)].pk for num in split_command if num.isnumeric()]
            print(list_range)
            playlist_name = str(split_command[-1].replace("name=",""))
            user.create_playlist(playlist_name,list_range)

        if "listplaylist." in run_command:
            [print(index.name,"\n",[con.name for con in index.content_list]) for index in user.current_category.playlist_lists]

        if "appendplaylist." in run_command:
            list_range = [user.current_category.content_list[int(num)] for num in split_command if num.isnumeric()]
            print(list_range)
            playlist_name = str(split_command[-1].replace("name=",""))
            found_pl = [pl for pl in user.current_category.playlist_lists if pl.name == playlist_name][0]
            [write_query(settings.PLAYLIST_CONTENT_TABLE,[found_pl.pk,item.pk]) for item in list_range]
    else:
        print("please try again")
        return
    return
