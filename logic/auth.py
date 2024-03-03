from typing import Tuple
import bcrypt

'''
This file handles the authentication of the user. 
It checks if a user is matched to an invoke function.
'''


def hash_password(password: str) -> str:
    '''
    Hash password using bcrypt for security
    '''
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    '''
    Check if the password matches the hashed password
    '''
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
