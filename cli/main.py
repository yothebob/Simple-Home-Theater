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
    return int(user_input)


def main_page():
    print("""
        type a command in:
    """)
    user_input = input(": ")
    if user_input.lower() is "help":
        print("""
        commands:
            category - go to your categories list
            add - add new category
            reload - reload category
            watched - show list of played content
            passwd - change password
        """)
    if user_input.lower() is "category":
        pass
    return

def run_app():
    user = home_page()
    user_categories = user.load_categories()
    picked_category = user_categories[show_user_categories(user_categories)]
    print("""Category contents:
            type the number, then type ...
            play - play contents
            checkout - see content metadata
    """)
    [print(index, ": ", picked_category.load_category_contents()[index].name) for index in range(len(picked_category.load_category_contents()))]
    user_input = input(": ")

run_app()
# category_contents[0].play_content()
