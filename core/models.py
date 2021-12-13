import os
import sys
from core.orm import query, write_query, delete_query
import core.core_settings as settings

class User():

    def __init__(self):
        self.categories = []
        self.watched = []
    # categories_list= []


    def save_user(self):
        #in progress
        pass
        # category_pks = [category.pk for category in self.categories]
        # write_query(settings.PROJECT_FILEPATH + "/data/users.csv",[self.pk,self.username,self.password,category_pks,self.watched],new=False,pk=self.pk)
        # load = query(settings.PROJECT_FILEPATH + "/data/users.csv", pk, "pk")
        # user = User()
        # user.pk = load[0]
        # user.username = load[1]
        # user.password = load[2]
        # user.categories = load[3]
        # user.watched = list(load[4])


    def add_category(self):
        ''' a function for pointing to a file for a category '''

        name = input("What is the name of the New Category?: ")
        folder_location = input("What is the path the the folder?: ")
        write_query(settings.PROJECT_FILEPATH + "/data/categories.csv", [self.pk,name,self.username,folder_location])
        load_category_list = query(settings.PROJECT_FILEPATH + "/data/categories.csv",name,"name")
        category = self.load_category(load_category_list)
        # self.save_user()
        category.write_category_contents()
        return



    def load_categories(self):
        '''
        return all user categories
        '''
        categories_query_list = query(settings.PROJECT_FILEPATH + "/data/categories.csv",self.pk,"fk","find all")
        # print(categories_query_list)
        for category in categories_query_list:
            self.categories.append(self.load_category(category))
        # print(self.categories_list)
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


    def append_watched(self,content):
        ''' get list of watched movies per username'''
        print(type(self.watched))
        self.watched.append(content.pk)
        return

    def get_categories(self):
        '''get list of category objects the user has'''
        pass

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


    def write_category_contents(self):
        '''
        for initial writing to db
        Create content objects for (many to many relationship) a Category Object
        arg : content - instance of Category()
        '''
        for file in os.listdir(self.folder_location):
            write_query(settings.PROJECT_FILEPATH + "/data/contents.csv",[str(self.pk),str(file),"","","",""])
        return

    def load_category_contents(self):
        '''
        for loading exsisting category
        quering the db to load the Category object with contents
        '''
        load_contents = query(settings.PROJECT_FILEPATH + '/data/contents.csv',self.pk,"fk","find all")
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


class ContentList():
    '''
    this class will be like genres, a list of contents put together based off a common tag or something
    '''
    pass

class Genre():

    def __init__(self, category, name):
        self.category = category
        self.name = name


class Tag():

    def __init__():
        self.name = name
