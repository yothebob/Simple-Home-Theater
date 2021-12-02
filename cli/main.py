from cli.app import CliApp


app = CliApp()

def home_page():
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


def run_app():

    instance = app.login()

category_contents[0].play_content()
