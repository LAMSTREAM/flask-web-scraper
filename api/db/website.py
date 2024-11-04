
from api.db.models import db, Website
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


def website_exists_for_user(sub, website_index):
    """ Check if a website exists for a specific user. """
    return Website.query.filter_by(index=website_index, user_sub=sub).first() is not None


def create_website(sub, website_url, content, screenshot, question: str):
    """
    Create a new website record for the given user.

    Returns the new website object upon success.
    """
    try:
        # Create a new website record
        new_website = Website(website_url=website_url, user_sub=sub, website_content=content, website_preview=screenshot, questions=[question])
        db.session.add(new_website)
        db.session.commit()
        return new_website

    except SQLAlchemyError as e:
        db.session.rollback()
        raise e  # Raise the exception to be handled in the route


def get_websites_by_user_sub_without_get_the_analyses(sub):
    """
    Retrieve all websites for a given user sorted by modification time in descending order.

    Returns a list of website objects.
    """
    try:
        # Retrieve websites related to the user, sorted by mtime in descending order
        websites = Website.query.filter_by(user_sub=sub).order_by(desc(Website.mtime)).all()
        return websites

    except SQLAlchemyError as e:
        raise e  # Raise the exception to be handled in the route


def get_website_by_index_with_analyses(sub, index):
    """
    Retrieve website for a given user by given id.

    Returns a website object.
    """
    index = int(index)
    try:
        website = Website.query.filter_by(index=index, user_sub=sub).first()
        return website

    except SQLAlchemyError as e:
        raise e  # Raise the exception to be handled in the route
