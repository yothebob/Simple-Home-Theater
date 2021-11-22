import os
import sys


class Account():

    def __init__(self):
        self.watched = []
        self.categories = []


    def get_watched(self):
        ''' get list of watched movies per username'''

        pass


    def get_categories(self):
        '''get list of category objects the user has'''
        pass



class Category():

    def __init__(self,folder_location, name):
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

    def __init__(name, category, genre, tags):
        self.name = name
        self.category = category
        self.genre = genre
        self.tags = tags
