
from api.db.models import db, Analysis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


def create_analysis(sub, website_index, question, answer):
    """
    Create a new analysis record.

    Returns the new analysis object upon success.
    """
    try:
        # Create a new analysis record
        new_analysis = Analysis(question=question, answer=answer, website_index=website_index)
        db.session.add(new_analysis)
        db.session.commit()
        return new_analysis

    except SQLAlchemyError as e:
        db.session.rollback()
        raise e  # Raise the exception to be handled in the route

def get_analyses_by_website(website_index):
    """
    Retrieve all analyses for a given website index.

    Returns a list of analysis objects.
    """
    try:
        # Query to get all analyses for the given website index
        analyses = Analysis.query.filter_by(website_index=website_index).order_by(desc(Analysis.index)).all()
        return analyses

    except SQLAlchemyError as e:
        raise e  # Raise the exception to be handled in the route