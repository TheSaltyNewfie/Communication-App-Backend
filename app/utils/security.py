import bcrypt
import secrets


def hashPassword(password: str):
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def checkPassword(password: str, hash: str):
    return bcrypt.checkpw(password.encode(), hash.encode())


def generateToken(length):
    token = secrets.token_urlsafe(length)
    return token
