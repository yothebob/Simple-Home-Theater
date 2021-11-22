from models import Category, Genre, Tag
import flaskapp


def query(filename, argument):
    '''a very simple function for returning a line from a csv (place holder for real db query)'''
    for line in filename:
        if argument in line:
            return line


def create_user():
    '''create and save a new user to database '''
    #maybe i should store them as .lower() and as regular (so I know if there is just a caps problem)?
    username = input("Username: ")
    password = input("Password: ")
    password_again = input("Password: ")
    username_taken = query("accounts.csv",username)

    while username_taken is not None:
        username = input("Username: ")

    while password is not password_again:
        password = input("Password: ")
        password_again = input("Password: ")

    database = open("accounts.csv", "a")
    categories = []
    watched = []
    database.write(f"{username},{password},{categories},{watched},\n)
    database.close()


def login(username, password):
    username = input("Username: ")
    password = input("Password: ")

    verify_credidentials = query("accounts.csv", username)

    if verify_credidentials is not None:
        #user found, attempting to authenticate
        if verify_credidentials[0] == username and verify_credidentials[1] == password:
            '''take to movie screen'''
            return
        else:
            return "User name or password not correct! please try again!"
    else:
        #query could not find user
        return "Cound not find username, please try again"


class Account():

    def load_user(self, username):
        return query("accounts.csv", username)


    def get_watched(self):
        ''' get list of watched movies per username'''

        pass


    def get_categories(self):
        '''get list of category objects the user has'''
        pass


def test_run():
    test_user = Account()
    test_user.create_user()
