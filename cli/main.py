from cli.app import CliApp


app = CliApp()

def home_page():
    '''welcome screen function and login/create user functionality'''
    print("""
        SIMPLE HOME THEATER

        type 'login' to login as existing user.
        type 'create' to create new user.
        """)
    user_input = input(": ")
    if user_input.lower() == "login":
        return app.login()
    elif user_input.lower() == "create":
        app.create_user()
        return app.login()


def show_user_categories(user_categories):
    print("user categories:")
    [print(index,": ",user_categories[index].name) for index in range(len(user_categories))]
    print("type a number to pick a category:\n")
    user_input = input(": ")
    return user_categories[int(user_input)]


def show_category_bins(category):
    "This function will be for creating new categories on the fly based off tags and other metadata, i hope to dynamically make these"
    pass


def show_category_contents(category):
    "This will just show all contents for now"
    print("""Category contents:
            type the number, then type ...
            play - play contents
            checkout - see content metadata
    """)
    category_contents = category.load_category_contents()
    [print(index, ": ", category_contents[index].name) for index in range(len(category_contents))] ## TODO: for some reason this is printing too many, but the length is fine?
    user_input = input(": ")
    # return int(user_input)
    return category_contents[int(user_input)]


def main_page(user):
    print("""
        type a command in:
    """)
    user_input = input(": ")
    if user_input.lower() == "help":
        print("""
        commands:
            category    - go to your categories list
            add         - add new category
            reload      - reload category
            watched     - show list of played content
            passwd      - change password
            exit        - exit program
        """)
        return main_page(user)
    elif user_input.lower() == "category":
        user_categories = user.load_categories()
        picked_category = show_user_categories(user_categories)
        picked_content = show_category_contents(picked_category)
        user.append_watched(picked_content)
        picked_content.play_content()
        # return main_page(user)
    elif user_input.lower() == "add":
         user.add_category()
         return main_page(user)
    elif user_input.lower() == "reload":
        #return user. # this needs to reload the category contents and rename and items and etc, erase any that have been removed, add any new items
        return main_page(user)
    elif user_input.lower() == "watched":
        user.get_watched()
        return main_page(user)
    elif user_input.lower() == "passwd":
        user.change_password()
        return main_page(user)
    elif user_input.lower() == "exit":
        exit()

    else:
        print("Sorry please try Again")
        return main_page(user)

def run_app():
    user = home_page()
    main_page(user)
    print(user.watched)
    

run_app()
