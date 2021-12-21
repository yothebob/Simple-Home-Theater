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


    def add_category(self):
        ''' a function for pointing to a file for a category '''

        name = input("What is the name of the New Category?: ")
        folder_location = input("What is the path the the folder?: ")
        write_query(settings.CATEGORY_TABLE, [self.pk,name,self.username,folder_location])
        load_category_list = query(settings.CATEGORY_TABLE,name,"name")
        category = self.load_category(load_category_list)
        # self.save_user()
        category.write_category_contents()
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


    def create_playlist(self,type="recent",size=10):
        '''a function for creating any playlist (maybe another function for customized ones)'''
        if type == "recent":
            playlist = PlayList()
            playlist.name = "Recently Played"
            # playlist.user = self.username
            for index in range(len(self.watched_content)):
                playlist.content_list.append(self.watched_content[index])
            # print(playlist.name)
            # [print(playlist_content.name) for playlist_content in playlist.content_list]
        self.playlist_stack.append(playlist)


    def sync_categories(self):
        for category in self.categories:
            category.sync()



    def change_password(self):
        old_password = input("Old Password:")
        new_password = input("New Password: ")
        new_password_again = input("Password Again: ")

        if new_password == new_password_again:
            self.password = new_password
        else:
            print("passwords did not match please try again")
        return


class Category():

    # def __init__(self, user, folder_location, name):

    def __init__(self):
        self.pk = 0
        self.fk = 0
        self.user = ""
        self.folder_location = ""
        self.name = ""
        self.content_list = []


    def load_content(self,list):
        instance = Content()
        # print("load_content_list: ",list)
        instance.pk = list[0]
        instance.fk = list[1]
        instance.name = list[2]
        instance.category = self
        instance.type = list[4]
        instance.genre = list[5]
        instance.tags = list[6]
        return instance


    def sync(self):
        find_files = query(settings.CONTENT_TABLE,self.pk,"fk","find all")
        found = 0
        not_found = 0
        for file in os.listdir(self.folder_location):
            find_file = query(settings.CONTENT_TABLE,file,"name")
            if find_file is not None:
                found += 1
            else:
                write_query(settings.CONTENT_TABLE,[self.fk,str(file),"","","",""])
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

    def play_content(self):
        # self.category.user.watched.append(self.pk)
        return os.system(f'{settings.MEDIA_PLAYER} {self.category.folder_location}/"{self.name}"')

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
