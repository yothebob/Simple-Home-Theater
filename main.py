from models import Category, Account, Genre, Tag, Content
import flaskapp
from orm import query, write_query, delete_query



#
# User managment
#




def create_user():
    '''create and save a new user to database '''
    #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
    print("creating user")

    username = input("Username: ")
    password = input("Password: ")
    password_again = input("Password: ")
    username_taken = query("accounts.csv",username)
    if username_taken is not None:
        while username_taken[0] == username:
            print("username taken")
            username = input("Username: ")
            password = input("Password: ")
            password_again = input("Password: ")
            username_taken = query("accounts.csv",username)

    while password != password_again:
        print("not matching passwords, please try again")
        password = input("Password: ")
        password_again = input("Password: ")

    write_query("accounts.csv",[username,password,[],[]])



def login():
    print("login")
    username = input("Username: ")
    password = input("Password: ")

    verify_credidentials = query("accounts.csv", username)
    print("verify", verify_credidentials)
    if verify_credidentials is not None:
        #user found, attempting to authenticate
        if verify_credidentials[0] == username and verify_credidentials[1] == password:
            instance = load_user(username)
            print(instance.password)
            '''take to movie screen'''
            print("logged in")
            return instance
        else:
            print("User name or password not correct! please try again!")
            return
    else:
        #query could not find user
        print("Cound not find username, please try again")
        return



def delete_user():
    print("deleting user...")
    username = input("Username:")
    password = input("Password:")
    password_again = input("Password:")

    if password == password_again:
        verify_username = query("accounts.csv",username)
        verify_password = query("accounts.csv", password)

    if verify_username is not None and verify_password is not None:
        delete_query("accounts.csv")



def load_user(username):
    # return query("accounts.csv", username)
    load = query("accounts.csv", username)
    user = Account()
    user.username = load[1]
    user.password = load[2]
    user.categories = load[3]
    user.watched = load[4]
    return user




#
# Category managment
#

def add_category():
    ''' a function for pointing to a file for a category '''
    name = input("What is the name of the New Category?: ")
    folder_location = input("What is the path the the folder?: ")
    write_query("categories.csv", [name,folder_location])
    return


def load_category(name):
    load = query("categories.csv",name)
    category = Category()
    category.name = load[1]
    category.folder_location = load[2]
    return category













#       FOR TESTING PURPOSES
#



def test_run():
    # create_user()
    instance = login()
    # print(test_user.watched,test_user.categories)
    # print(test_user.username,test_user.password)


test_run()
