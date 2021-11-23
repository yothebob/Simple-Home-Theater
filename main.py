from models import Category, Account, Genre, Tag, Content
import flaskapp


def query(filename, argument):
    '''a very simple function for returning a line from a csv (place holder for real db query)'''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            line_array = [item for item in line.split(",")]
            for column in line_array:
                if column == argument:
                    print(line_array)
                    print(line_array[0])
                    f.close()
                    return line_array



def delete_query(filename, argument ,amount="all"):
    '''a simple function for deleting a whole column if amount is set to "all"
    or just a single argument '''
    f = open(filename, 'r')
    for line in f:
        if argument in line:
            if amount == "full":
                line_array = [item == None for item in line.split(",")] #delete while line/row
                print(line_array)
                print(line_array[0])
                return line_array
            else:
                line_array = [item for item in line.split(",") if item != argument]
                print(line_array)
                print(line_array[0])
                return line_array



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
    user.username = load[0]
    user.password = load[1]
    user.categories = load[2]
    user.watched = load[3]
    return user


def add_content():
    pass

#
#       FOR TESTING PURPOSES
#



def test_run():
    # create_user()
    instance = login()
    # print(test_user.watched,test_user.categories)
    # print(test_user.username,test_user.password)


test_run()
