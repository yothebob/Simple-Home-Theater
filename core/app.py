from core.models import Category, User, Genre, Tag, Content
# import flaskapp
from core.orm import query, write_query, delete_query
import core.core_settings as settings


# def load_object(db_name,query_argument,object,object_variables):
#     '''
#     a generic function for loading any object, to be made more unique by specializing functions.
#     querys a list based off query_argument and db_name, then writes to object_variables , then returns loaded instance
#     db_name: (str) name of filename ex: data/users.csv
#     query_argument: (str) an arguement to search for
#     object: (class) pass the class to make an instance of
#     object_variables: (list of variables) a list of the object_variables that will get loaded with query data. THIS NEEDS TO BE IN THE SAME ORDER AS THE DB COLUMNS
#     '''
#     data = query(db_name,query_argument)
#     instance = object()
#     for index in range(len(data)):
#         if len(object_variables) >= index and len(data) >= index:
#             instance.object_variables[index] = data[index]
#     return instance




#
# User managment
#

class App():
    '''
    a class for managing the core app, doing admin thing and etc
    '''


    def create_user(self,username,password,password_again):
        '''create and save a new user to database '''
        #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
        username_taken = query(settings.PROJECT_FILEPATH +"/data/users.csv",username)
        if username_taken is not None:
            if username_taken[1] == username:
                return # username taken
        if password != password_again:
            return # passwords dont match
        write_query(settings.PROJECT_FILEPATH + "/data/users.csv",[username,password,[],[]])


    def login(self,username,password):
        verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                instance = self.load_user(verify_credidentials[0])
                '''take to movie screen'''
                return instance
            else:
                #not right credidentials
                return
        else:
            #query could not find user
            return


    def delete_user(self,username,password,password_again):
        if password == password_again:
            verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
        if verify_credidentials:
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                delete_query(settings.PROJECT_FILEPATH + "/data/users.csv",username)
                return
        return


    def load_user(self,pk):
        load = query(settings.PROJECT_FILEPATH + "/data/users.csv", pk, "pk")
        user = User()
        user.pk = load[0]
        user.username = load[1]
        user.password = load[2]
        user.categories = load[3]
        user.watched = load[4]
        return user
