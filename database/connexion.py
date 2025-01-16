from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "sqlite:///contacts.db"


def get_engine():
    return create_engine(url=db_url)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
