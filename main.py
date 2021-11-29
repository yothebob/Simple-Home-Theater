from models import Category, User, Genre, Tag, Content
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
    username_taken = query("data/users.csv",username)
    if username_taken is not None:
        while username_taken[0] == username:
            print("username taken")
            username = input("Username: ")
            password = input("Password: ")
            password_again = input("Password: ")
            username_taken = query("data/users.csv",username)

    while password != password_again:
        print("not matching passwords, please try again")
        password = input("Password: ")
        password_again = input("Password: ")

    write_query("data/users.csv",[username,password,[],[]])



def login():
    print("login")
    username = input("Username: ")
    password = input("Password: ")

    verify_credidentials = query("data/users.csv", username)
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
        verify_username = query("data/users.csv",username)
        verify_password = query("data/users.csv", password)

    if verify_username is not None and verify_password is not None:
        delete_query("data/users.csv")



def load_user(username):
    # return query("data/users.csv", username)
    load = query("data/users.csv", username)
    user = User()
    user.pk = load[0]
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
    write_query("data/categories.csv", [name,folder_location])
    return


def load_category(pk):
    load = query("data/categories.csv",pk)
    category = Category()
    category.pk = load[0]
    category.name = load[1]
    category.folder_location = load[2]
    return category


def write_category_contents(category):
    '''
    for initial writing to db
    Create content objects for (many to many relationship) a Category Object
    arg : content - instance of Category()
    '''
    for file in os.listdir(category.filename):
        write_query("data/contents.csv",[str(category.pk),str(file),[],[],[],[]])
    return

def load_category_contents(category):
    '''
    for loading exsisting category
    quering the db to load the Category object with contents
    '''
    load_contents = query('data/categories_contents.csv',category.pk,"fk","find all")
    category_contents_list = []
    for item in load_contents:





def load_content(data):
    instance = Content()
    instance.pk = data[0]
    instance.fk = data[1]
    isntance.name = data[2]
    instance.category = data[3]
    instance.type = data[4]
    instance.genre = data[5]
    instance.tags = data[6]






#       FOR TESTING PURPOSES
#



def test_run():
    # create_user()
    instance = login()
    # print(test_user.watched,test_user.categories)
    # print(test_user.username,test_user.password)


test_run()
