from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from random import shuffle

from exceptions import UserAlreadyExistsError, UserNotExistsError

engine = create_engine('sqlite:///./santa.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
ses = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    partner_id = Column(Integer)


Base.metadata.create_all(engine)


def get_by_id(user_id: int):
    return ses.query(User).filter(User.user_id == user_id).first()


def get_all_user_id():
    list_of_users_id = []
    for x in ses.query(User.user_id).all():
        list_of_users_id.append(*x)
    return list_of_users_id


def add_user_to_db(first_name: str, last_name: str, username: str, user_id: int):
    user_model = User
    if not get_by_id(user_id):
        new_user = user_model(first_name=first_name, last_name=last_name, username=username, user_id=user_id)
        ses.add(new_user)
        ses.commit()
    else:
        raise UserAlreadyExistsError


def delete_user_from_db(user_id: int):
    user = get_by_id(user_id)
    if user:
        ses.delete(user)
        ses.commit()
    else:
        raise UserNotExistsError


def randomizer():
    list_of_users_id = get_all_user_id()
    shuffle(list_of_users_id)
    length = len(list_of_users_id)
    for i in range(len(list_of_users_id)):
        ses.query(User).filter(User.user_id == list_of_users_id[i]).update(
            {'partner_id': list_of_users_id[(i + 1) % length]})
        ses.commit()
