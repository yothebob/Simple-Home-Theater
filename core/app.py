from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings


#
# User managment
#

class App():
    '''
    a class for managing the core app, doing admin thing and etc
    '''

    def __init__(self):
         self.user = User

    def autoreplay(self):
        '''
        This is the auto countdown timer for playing the next content
        '''
        sleep(settings.AUTOPLAY_COUNTDOWN)
        return True


    def create_user(self,username,password,password_again):
        '''create and save a new user to database '''
        #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
        error = ""
        username_taken = query(settings.USER_TABLE,username)
        if username_taken is not None:
            if username_taken[1] == username:
                # username taken
                error = ("user_taken","Username Taken.")
                return error
        if password != password_again:
            # passwords dont match
            error = ("unmatched_password","Passwords don't match, please try again.")
            return error
        else:
            write_query(settings.USER_TABLE,[username,password,"",""])
            # return self.login()


    def login(self,username,password):
        error = ""
        verify_credidentials = query(settings.USER_TABLE, username)
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                instance = self.load_userz(verify_credidentials[0])
                '''take to movie screen'''
                return instance
            else:
                #not right credidentials
                error = ("wrong_password","Username of Password<h3>{{category}}</h3> is not correct.")
                return error
        else:
            #query could not find user
            error = ("no_user","Could not find user")
            return error


    def delete_user(self,username,password,password_again):
        if password == password_again:
            verify_credidentials = query(settings.USER_TABLE, username)
        if verify_credidentials:
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                delete_query(settings.USER_TABLE,username)
                return
        return


    def load_userz(self,pk):
        load = query(settings.USER_TABLE, pk, "pk")
        [print(index,load[index]) for index in range(len(load))]
        user = User()
        user.pk = load[0]
        user.id = load[0]
        user.username = load[1]
        user.password = load[2]
        user.load_categories()
        user.load_watched()
        return user
