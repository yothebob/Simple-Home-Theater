import os
import sys


class User():

    def __init__(self):

        self.watched = []
        self.categories = []


    def add_category(self):
        ''' a function for pointing to a file for a category '''
        name = input("What is the name of the New Category?: ")
        folder_location = input("What is the path the the folder?: ")
        user = self.username
        write_query("data/categories.csv", [name,user,folder_location])
        return



    def get_watched(self):
        ''' get list of watched movies per username'''

        pass


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

    def __init__(self, user, folder_location, name):
        self.pk = 0
        self.user = user
        self.folder_location = folder_location
        self.name = name


class Genre():

    def __init__(self, category, name):
        self.category = category
        self.name = name


class Tag():

    def __init__():
        self.name = name

class Content():
    '''a base class that will store any piece of media content, and hold relationships to its
    tags, categories, genre, type and etc'''
    def __init__(name, category, type, genre, tags):
        self.name = name
        self.category = category
        self.type = type
        self.genre = genre
        self.tags = tags

    description = ""
    rating = 0
