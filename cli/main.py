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


def run_app():
    user = home_page()
    user_categories = user.load_categories()
    picked_category = user_categories[show_user_categories(user_categories)]
    print(picked_category.load_category_contents())

run_app()
# category_contents[0].play_content()
