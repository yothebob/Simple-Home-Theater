from getpass import getpass
from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from time import sleep

class CliApp(App):
    '''
    a class for managing the cli app, doing admin thing and etc
    '''

    def home_page(self):
        '''welcome screen function and login/create user functionality'''
        print("""
            {}

            type in a username to login as existing user, or type 'login'.
            type 'create' to create new user.
            type 'delete' to delete user.
            type 'change' to change username/password.
            

            """.format(settings.APP_NAME))
        user_input = input(": ")
        if user_input.lower() == "login":
            return self.login()
        elif user_input.lower() == "create":
            self.create_user()
            return self.login()
        elif user_input.lower() == "exit":
            return self.logout()
        elif user_input.lower() == "delete":
            return self.delete_user()
        elif user_input.lower() == "change":
            return self.change_password()
        else:
            find_username = query(settings.USER_TABLE,self.encrypt(user_input))
            if find_username is not None:
                if self.encrypt(user_input) == find_username[1]:
                    return self.login(user_input)
            else:
                print("Please try again...")
                return self.home_page()


    def create_user(self):
        '''create and save a new user to database '''
        #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
        print("creating user")
        username = input("Username: ")
        # password = input("Password: ")
        # password_again = input("Password: ")
        password = getpass("Password: ")
        password_again = getpass("Password: ")
        username_taken = query(settings.USER_TABLE,username)
        if username_taken is not None:
            while username_taken[1] == username:
                print("username taken")
                username = input("Username: ")
                password = getpass("Password: ")
                password_again = getpass("Password: ")
                username_taken = query(settings.USER_TABLE,username)

        while password != password_again:
            print("not matching passwords, please try again")
            password = getpass("Password: ")
            password_again = getpass("Password: ")

        write_query(settings.USER_TABLE,[username,password,"",""])



    def login(self,username=""):
        print("login:\n")
        if username == "":
            username = input("Username: ")
        else:
            username = username
        # password = input("Password: ")
        password = getpass("Password: ")

        verify_credidentials = query(settings.USER_TABLE, self.encrypt(username))
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == self.encrypt(username) and verify_credidentials[2] == self.encrypt(password):
                instance = self.load_userz(verify_credidentials[0])
                '''take to movie screen'''
                print("logged in...\n")
                return instance
            else:
                print("User name or password not correct! please try again!\n")
                return self.login()
        else:
            #query could not find user
            print("Cound not find username, please try again...\n")
            return self.login()



    def logout(self):
        print('''logging out...
           {}
        '''.format(settings.GOODBYE))



    def delete_user(self):
        print("deleting user...\n")
        username = input("Username:")
        password = getpass("Password: ")
        password_again = getpass("Password: ")

        if password == password_again:
            verify_password = query(settings.USER_TABLE, password)
            verify_username = query(settings.USER_TABLE,username)

        if verify_username is not None and verify_password is not None:
           write_query(settings.USER_TABLE,new=False,where={"username" : username ,"password" : password})


    def change_password(self):
        print("Changing Password...\n")
        username = input("Username:")
        password = getpass("Password: ")
        password_again = getpass("Password: ")

        if password == password_again:
            verify_password = query(settings.USER_TABLE, password)
            verify_username = query(settings.USER_TABLE,username)

        if verify_username is not None and verify_password is not None:
            new_username = input("New Username: ")
            new_password = input("New Password: ")
            new_password_again = input("Password Again: ")
            if new_password == new_password_again:
                write_query(settings.USER_TABLE,arguments=[new_username,new_password],new=False,where={"username" : username ,"password" : password})
