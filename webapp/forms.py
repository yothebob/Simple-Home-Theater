from wtforms import Form, SelectField, SubmitField, validators, RadioField,StringField

class LoginForm(Form):

    username = StringField("Username:")
    password = StringField("Password:")
    submit = SubmitField("Log In")

class CreateUserForm(Form):

    username = StringField("Username:")
    password = StringField("Password:")
    password_again = StringField("Password again:")
    submit = SubmitField("Create User")

class AddCategoryForm(Form):
    name = StringField("Category Name:")
    filepath = StringField("filepath:")
    submit = SubmitField("Add Category")
