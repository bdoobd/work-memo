from routers import users
from models.user import User
from sqlmodel import Session, select, col
from database import engine


def create_user():
    user1 = User(username="admin", role_id=1, password_hash="hash1")
    user2 = User(username="power", role_id=2, password_hash="hash2")
    user3 = User(username="user", role_id=3, password_hash="hash3")
    user4 = User(username="goga", role_id=3, password_hash="hash4")
    user5 = User(username="mana", role_id=3, password_hash="hash5")
    user6 = User(username="peppa", role_id=2, password_hash="hash6")
    user7 = User(username="mabuta", role_id=3, password_hash="hash7")
    user8 = User(username="coor", role_id=3, password_hash="hash8")
    user9 = User(username="yaba-daba-doo", role_id=3, password_hash="hash9")

    with Session(engine) as session:
        session.add(user1)
        session.add(user2)
        session.add(user3)
        session.add(user4)
        session.add(user5)
        session.add(user6)
        session.add(user7)
        session.add(user8)
        session.add(user9)

        session.commit()


def get_all_users():
    with Session(engine) as session:
        # stmt = select(User)
        # users = session.exec(stmt)
        users = session.exec(select(User).offset(6).limit(4)).all()

        # return users.all()
    return users


def get_user_by_id(user_id: int):
    with Session(engine) as session:
        # user = session.exec(select(User).where(User.id == user_id)).first()
        user = session.get(User, user_id)

    return user


def get_user_by_name():
    with Session(engine) as session:
        stmt = select(User).where(col(User.id).in_([33, 34, 35]))
        user = session.exec(stmt).all()

    return user


def update_user_by_id(id: int, password: str):
    with Session(engine) as session:
        # user = session.get(User, id)
        stmt = select(User).where(User.id == id)
        user = session.exec(stmt).first()

        if user is None:
            return None  # FIXME: Можно было бы сделать исключение и обработать его в роутере, чтобы возвращать 404 статус

        user.password_hash = password
        session.add(user)
        session.commit()

        return user.username


def delete_user(id: int):
    with Session(engine) as session:
        user = session.get(User, id)

        session.delete(user)
        session.commit()

        return user
