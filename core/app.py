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

    def autoreplay(self):
        '''
        This is the auto countdown timer for playing the next content
        '''
        sleep(settings.AUTOPLAY_COUNTDOWN)
        return True


    def create_user(self,username,password,password_again):
        '''create and save a new user to database '''
        #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
        username_taken = query(settings.PROJECT_FILEPATH +settings.USER_TABLE,username)
        if username_taken is not None:
            if username_taken[1] == username:
                return # username taken
        if password != password_again:
            return # passwords dont match
        write_query(settings.PROJECT_FILEPATH + settings.USER_TABLE,[username,password,"",""])


    def login(self,username,password):
        verify_credidentials = query(settings.PROJECT_FILEPATH + settings.USER_TABLE, username)
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
            verify_credidentials = query(settings.PROJECT_FILEPATH + settings.USER_TABLE, username)
        if verify_credidentials:
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                delete_query(settings.PROJECT_FILEPATH + settings.USER_TABLE,username)
                return
        return


    def load_user(self,pk):
        load = query(settings.PROJECT_FILEPATH + settings.USER_TABLE, pk, "pk")
        [print(index,load[index]) for index in range(len(load))]
        user = User()
        user.pk = load[0]
        user.username = load[1]
        user.password = load[2]
        user.load_categories()
        user.load_watched()
        return user
