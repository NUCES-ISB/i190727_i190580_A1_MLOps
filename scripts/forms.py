# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class LoginForm(Form):
    """
    This is a class definition for a Flask form named LoginForm. It inherits from the Form class provided by the wtforms library.

    The form contains three fields: username, password, and email, each represented by a StringField object.

    Validators are applied to each field to ensure that they meet certain requirements. The username and password fields are required and must be between 1 and 30 characters long. The email field is optional and must be between 0 and 50 characters long.

    Overall, this form is intended for use in a login or signup page in a Flask web application.
    """
    username = StringField('Username:', validators=[validators.DataRequired(), 
                                                    validators.Length(min=1, max=30)])
    password = StringField('Password:', validators=[validators.DataRequired(), 
                                                    validators.Length(min=1, max=30)])
    email = StringField('Email:', validators=[validators.optional(), 
                                              validators.Length(min=0, max=50)])
