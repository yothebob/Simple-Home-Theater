import os
import sys
import math
import subprocess
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from datetime import datetime

class User():

    def __init__(self):
        self.categories = []
        self.watched = []
        self.watched_content = []
        self.current_category = ""
        self.playlist_stack = []


    def add_category(self,name,folder_location):
        ''' a function for pointing to a file for a category '''
        write_query(settings.CATEGORY_TABLE, [self.pk,name,self.username,folder_location])
        load_category_list = query(settings.CATEGORY_TABLE,name,"name")
        category = self.load_category(load_category_list)
        # self.save_user()
        category.write_category_contents()
        return

    def recursive_add_category(self,name,folder_location):
        ''' a function for pointing to a file for a category '''
        write_query(settings.CATEGORY_TABLE, [self.pk,name,self.username,folder_location])
        load_category_list = query(settings.CATEGORY_TABLE,name,"name")
        category = self.load_category(load_category_list)
        # self.save_user()
        category.recursive_write_category_contents()
        return

    def load_categories(self):
        '''
        return all user categories
        '''
        categories_query_list = query(settings.CATEGORY_TABLE,self.pk,"fk","find all")
        self.categories = []
        for category in categories_query_list:
            self.categories.append(self.load_category(category))
        return self.categories


    def load_category(self, list):
        category = Category()
        category.pk = list[0]
        category.fk = list[1]
        category.name = list[2]
        category.user = list[3]
        category.folder_location = list[4]
        category.load_category_contents()
        category_playlists = query(settings.PLAYLIST_TABLE,category.pk,"category_fk","find all")
        print(category_playlists)
        [category.load_playlist(playlist_list) for playlist_list in category_playlists]

        # [category.load_playlist(playlist_list]) for playlist_list in category_playlists]
        return category


    def load_watched(self):
        ''' loads watched from DB, created watched objects and content objects. saves both in user lists'''
        watched = query(settings.WATCH_TABLE,self.pk,"user_pk","find all")
        # print(watched)
        if watched is not None:
            for item in watched:
                watched_instance = Watch(item[0],item[1],item[2],item[3])
                self.watched_content.append(watched_instance.content)
                self.watched.append(watched_instance)
        # [print(watch.name) for watch in self.watched_content]
        return


    def append_watched(self,content):
        ''' get list of watched movies per username'''
        # print(type(self.watched))
        self.watched.append(content.pk)
        write_query(settings.WATCH_TABLE, [self.pk,content.pk,datetime.now()])
        return


    def create_playlist(self,name="recent",playlist_list=[],size=10):
        '''a function for creating any playlist (maybe another function for customized ones)'''
        if name == "recent":
            playlist = PlayList()
            playlist.name = "Recently Played"
            playlist.user = self.pk
            for index in range(len(self.watched_content)):
                playlist.content_list.append(self.watched_content[index])
        else:
            playlist = PlayList()
            playlist.name = name
            playlist.user = self.pk
            write_query(settings.PLAYLIST_TABLE,[self.pk,name,self.current_category.pk])
            new_playlist = query(settings.PLAYLIST_TABLE,playlist.name,"name")
            [playlist.content_list.append(item) for item in playlist_list]
            [write_query(settings.PLAYLIST_CONTENT_TABLE,[new_playlist[0],item]) for item in playlist_list]
        self.playlist_stack.append(playlist)



    def sync_categories(self):
        for category in self.categories:
            category.sync()

    def recursive_sync_categories(self):
        for category in self.categories:
            category.recursive_sync()


    def change_password(self,old_password,new_password,new_password_again):
        if new_password == new_password_again:
            self.password = new_password
            write_query(settings.USER_TABLE,[new_password],False,self.pk)
        else:
            print("passwords did not match please try again")
        return


class Category():

    # def __init__(self, user, folder_location, name):

    def __init__(self):
        self.pk = 0
        self.fk = 0 #user pk
        self.user = ""
        self.folder_location = ""
        self.name = ""
        self.content_list = []
        self.playlist_lists = []


    def load_content(self,list):
        instance = Content()
        # print("load_content_list: ",list)
        instance.pk = list[0]
        instance.fk = list[1]
        instance.name = list[2]
        instance.category = self
        instance.subfolder = list[3]
        # instance.type = list[4]
        # instance.genre = list[5]
        # instance.tags = list[6]
        return instance


    def load_playlist(self,list):
        playlist = PlayList()
        playlist.pk = list[0]
        playlist.user_fk = list[1]
        playlist.name = list[2]
        new_playlist_content = query(settings.PLAYLIST_CONTENT_TABLE,playlist.pk,"playlist_fk","find all")
        content_data_list = [query(settings.CONTENT_TABLE,content_fk[2],"pk") for content_fk in new_playlist_content]
        playlist.category_fk = list[3]
        [playlist.content_list.append(self.load_content(content_data)) for content_data in content_data_list]
        self.playlist_lists.append(playlist)

    def sync(self):
        # this is NOT RECURSIVE , It should be made to have an option to be recursive
        find_files = query(settings.CONTENT_TABLE,self.pk,"fk","find all")
        found = 0
        not_found = 0
        for file in os.listdir(self.folder_location):
            find_file = query(settings.CONTENT_TABLE,file,"name")
            if find_file is not None:
                found += 1
            else:
                write_query(settings.CONTENT_TABLE,[self.pk,str(file),"","","",""])
                print(f"wrote {file}")
                not_found += 1
        print("found: ",found,"\nnot found: ",not_found)


    def recursive_sync(self):
        find_files = query(settings.CONTENT_TABLE,self.pk,"fk","find all")
        found = 0
        not_found = 0
        for file in os.listdir(self.folder_location):
            if os.path.isdir(self.folder_location + '/' + file):
                print("found folder")
                for subfile in os.listdir(str(self.folder_location + "/"+ file)):
                    # write_query(settings.CONTENT_TABLE,[str(self.pk),str("'" + subfile + "'"),str(file),"","",""])
                    find_file = query(settings.CONTENT_TABLE,subfile,"name")
                    if find_file is not None:
                        found += 1
                    else:
                        write_query(settings.CONTENT_TABLE,[str(self.pk),str("'" + subfile + "'"),str(file),"","",""])
                        print(f"wrote {file}")
                        not_found += 1
            else:
                find_file = query(settings.CONTENT_TABLE,file,"name")
            if find_file is not None:
                found += 1
            else:
                write_query(settings.CONTENT_TABLE,[self.pk,str(file),"","","",""])
                print(f"wrote {file}")
                not_found += 1
        print("found: ",found,"\nnot found: ",not_found)


    def write_category_contents(self):
        '''
        for initial writing to db
        Create content objects for (many to many relationship) a Category Object
        arg : content - instance of Category()
        '''
        for file in os.listdir(self.folder_location):
            write_query(settings.CONTENT_TABLE,[str(self.pk),str(file),"","","",""])
        return


    def recursive_write_category_contents(self):
        '''
        for initial writing to db
        Create content objects for (many to many relationship) a Category Object
        arg : content - instance of Category()
        '''
        for file in os.listdir(self.folder_location):
            if os.path.isdir(self.folder_location + '/' + file):
                print("found folder")
                for subfile in os.listdir(str(self.folder_location + "/"+ file)):
                    write_query(settings.CONTENT_TABLE,[str(self.pk),str("'" + subfile + "'"),str(file),"","",""])
            else:
                write_query(settings.CONTENT_TABLE,[str(self.pk),str(file),"","","",""])
        return

    def load_category_contents(self):
        '''
        for loading exsisting category
        quering the db to load the Category object with contents
        '''
        load_contents = query(settings.CONTENT_TABLE,self.pk,"fk","find all")
        # print(load_contents)
        for content in load_contents:
            # print("content: ",content)
            self.content_list.append(self.load_content(content))
        return self.content_list






class Content():
    '''a base class that will store any piece of media content, and hold relationships to its
    tags, categories, genre, type and etc'''
    # def __init__(name, category, type, genre, tags):
    pk = 0
    name = ""
    category = ""
    type = ""
    genre = ""
    tags = []
    description = ""
    rating = 0
    subfolder = ""

    def play_content(self):
        if self.subfolder is None:
            return os.system(f'{settings.MEDIA_PLAYER} {self.category.folder_location}/"{self.name}"')
        else:
            #content found recursively (subfolder)
            return os.system(f'{settings.MEDIA_PLAYER} {self.category.folder_location}/{self.subfolder}/"{self.name}"')

    #not working yet
    # def sec_to_hours(self,time):
    #     print(time)
    #     hours = math.floor(time/60)
    #     remainder = time - (hours * 60)
    #     return str(hours) + ":" + str(remainder)
    #
    #
    # @property
    # def play_length(self):
    #     result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
    #                              "format=duration", "-of",
    #                              "default=noprint_wrappers=1:nokey=1", f"{self.category.folder_location}/{self.name}"],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT)
    #     return str(self.sec_to_hours(math.floor(float(result.stdout))))

class PlayList():
    '''
    this class will be like genres, a list of contents put together based off a common tag or something
    (play lists will not be saved in the DB... as of right now)
    '''
    def __init__(self):
        self.user = ""
        self.user_fk = ""
        self.category_fk = ""
        self.name = ""
        self.content_list = []


class Genre():

    def __init__(self, category, name):
        self.category = category
        self.name = name


class Tag():

    def __init__():
        self.name = name


class Watch():

    def __init__(self,pk,user_pk,content_pk,date):
        self.pk = pk
        self.user_pk = user_pk
        self.content_pk = content_pk
        self.date = date

    @property
    def content(self):
        list = query(settings.CONTENT_TABLE, self.content_pk, "content_pk")
        instance = Content()
        instance.pk = list[0]
        instance.fk = list[1]
        instance.name = list[2]
        instance.type = list[4]
        instance.category= "" #
        instance.genre = list[5]
        instance.tags = list[6]
        return instance
