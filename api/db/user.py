
from api.db.models import db, User
from sqlalchemy.exc import SQLAlchemyError


def user_exists(sub):
    """
    Check if a user exists by their Auth0 sub.

    Returns True if the user exists, otherwise False.
    """
    return User.query.filter_by(sub=sub).first() is not None


def db_sync_user(sub, email):
    """
    Sync user information in the database.
    If the user exists, update their email; otherwise, create a new user.

    Returns the user object and a message indicating the action taken.
    """
    try:
        user = User.query.filter_by(sub=sub).first()

        if user:
            # Update existing user's email
            user.email = email
            message = "User updated successfully"
        else:
            # Create new user
            user = User(sub=sub, email=email)
            db.session.add(user)
            message = "User created successfully"

        # Commit the transaction
        db.session.commit()
        return user, message

    except SQLAlchemyError as e:
        # Roll back in case of an error
        db.session.rollback()
        raise e  # Raise the exception to be handled in the route

