from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings


class CliApp(App):
    '''
    a class for managing the cli app, doing admin thing and etc
    '''


    def create_user(self):
        '''create and save a new user to database '''
        #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
        print("creating user")

        username = input("Username: ")
        password = input("Password: ")
        password_again = input("Password: ")
        username_taken = query(settings.PROJECT_FILEPATH +"/data/users.csv",username)
        if username_taken is not None:
            while username_taken[1] == username:
                print("username taken")
                username = input("Username: ")
                password = input("Password: ")
                password_again = input("Password: ")
                username_taken = query(settings.PROJECT_FILEPATH + "/data/users.csv",username)

        while password != password_again:
            print("not matching passwords, please try again")
            password = input("Password: ")
            password_again = input("Password: ")

        write_query(settings.PROJECT_FILEPATH + "/data/users.csv",[username,password,[],[]])



    def login(self):
        print("login:\n")
        username = input("Username: ")
        password = input("Password: ")

        verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                instance = self.load_user(verify_credidentials[0])
                '''take to movie screen'''
                print("logged in...\n")
                return instance
            else:
                print("User name or password not correct! please try again!\n")
                return
        else:
            #query could not find user
            print("Cound not find username, please try again...\n")
            return



    def logout(self,user):
        '''
        '''
        print('''logging out...
            hope to see you again soon! :)
        ''')

        

    def delete_user(self):
        print("deleting user...\n")
        username = input("Username:")
        password = input("Password:")
        password_again = input("Password:")

        if password == password_again:
            verify_password = query(settings.PROJECT_FILEPATH + "/data/users.csv", password)
            verify_username = query(settings.PROJECT_FILEPATH + "/data/users.csv",username)

        if verify_username is not None and verify_password is not None:
            delete_query(settings.PROJECT_FILEPATH + "/data/users.csv",username)
