# -*- coding: utf-8 -*-

from scripts import tabledef
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt


@contextmanager
def session_scope():
    """
    Context manager that provides a transactional scope around a series of operations.
    Returns a session object from the sessionmaker bound to the database engine defined in tabledef.
    Any changes made within the session will be rolled back if an exception is raised, otherwise committed upon successful completion of the block of code within the with statement.
    """
    my_session = get_session()
    my_session.expire_on_commit = False
    try:
        yield my_session
        my_session.commit()
    except:
        my_session.rollback()
        raise
    finally:
        my_session.close()


def get_session():
    """
    Returns a session object from the sessionmaker bound to the database engine defined in tabledef.
    """
    return sessionmaker(bind=tabledef.engine)()


def get_user():
    """
    Returns the User object for the current session's user by querying the database for the user with a username that matches the session's username.
    Uses the session_scope context manager to safely query the database.
    """
    username = session['username']
    with session_scope() as my_session:
        user = my_session.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        return user


def add_user(username, password, email):
    """
    Adds a new user to the database.
    Takes in a username, password, and email.
    Uses the session_scope context manager to safely add the new user to the database.
    """
    with session_scope() as my_session:
        u = tabledef.User(username=username, password=password.decode('utf8'), email=email)
        my_session.add(u)
        my_session.commit()


def change_user(**kwargs):
    """
    Changes the information for the current session's user in the database.
    Takes in keyword arguments for any information that needs to be updated.
    Uses the session_scope context manager to safely update the user's information in the database.
    """
    username = session['username']
    with session_scope() as my_session:
        user = my_session.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        for arg, val in kwargs.items():
            if val != "":
                setattr(user, arg, val)
        my_session.commit()


def hash_password(password):
    """
    Takes in a password string and hashes it using bcrypt.
    Returns the hashed password.
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    """
    Checks if the given username and password match a user in the database.
    Uses bcrypt to compare the provided password with the user's stored hashed password.
    Returns True if the credentials are valid, False otherwise.
    Uses the session_scope context manager to safely query the database.
    """
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False


def username_taken(username):
    """
    Checks if a given username already exists in the database.
    Returns the User object if the username exists, None otherwise.
    Uses the session_scope context manager to safely query the database.
    """
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
