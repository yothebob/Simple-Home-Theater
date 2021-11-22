from models import Category, Account, Genre, Tag, Content
import flaskapp


def query(filename, argument):
    '''a very simple function for returning a line from a csv (place holder for real db query)'''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            f.close()
            return line


def create_user():
    '''create and save a new user to database '''
    #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
    print("creating user")

    username = input("Username: ")
    password = input("Password: ")
    password_again = input("Password: ")
    username_taken = query("accounts.csv",username)

    while username_taken == username and len(username) > 5:
        print("username taken")
        username = input("Username: ")

    while password != password_again:
        password = input("Password: ")
        password_again = input("Password: ")

    database = open("accounts.csv", "a")
    categories = []
    watched = []
    database.write(f"{username},{password},{categories},{watched},\n")
    database.close()



def login():
    print("login")
    username = input("Username: ")
    password = input("Password: ")

    verify_credidentials = query("accounts.csv", username)

    if verify_credidentials is not None:
        #user found, attempting to authenticate
        if verify_credidentials[0] == username and verify_credidentials[1] == password:
            current_account = load_user(username)
            print(current_account.password)
            '''take to movie screen'''
            return print("logged in")
        else:
            return print("User name or password not correct! please try again!")
    else:
        #query could not find user
        return print("Cound not find username, please try again") 


def load_user(username):
    # return query("accounts.csv", username)
    load = query("accounts.csv", username)
    user = Account()
    user.username = load[0]
    user.password = load[1]
    user.categories = load[2]
    user.watched = load[3]



#
#       FOR TESTING PURPOSES
#



def test_run():
    create_user()
    login()
    # print(test_user.watched,test_user.categories)
    # print(test_user.username,test_user.password)


test_run()
