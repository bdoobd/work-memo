from routers import users
from models.user import CreateUser, User, ShowUser
from models.role import Role
from sqlmodel import Session, select, col
from database import engine


def create_user():
    user1 = CreateUser(username="admin", role_id=1, password="hash1")
    user2 = CreateUser(username="power", role_id=2, password="hash2")
    user3 = CreateUser(username="user", role_id=3, password="hash3")
    user4 = CreateUser(username="goga", role_id=3, password="hash4")
    user5 = CreateUser(username="mana", role_id=3, password="hash5")
    user6 = CreateUser(username="peppa", role_id=2, password="hash6")
    user7 = CreateUser(username="mabuta", role_id=3, password="hash7")
    user8 = CreateUser(username="coor", role_id=3, password="hash8")
    user9 = CreateUser(username="yaba-daba-doo", role_id=3, password="hash9")

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


def add(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        return user


def read(offset: int, limit: int):
    with Session(engine) as session:
        users = session.exec(
            select(User).offset(offset=offset).limit(limit=limit)
        ).all()

        return users


#     with Session(engine) as session:
#         # stmt = select(User)
#         # users = session.exec(stmt)
#         users = session.exec(select(User).offset(6).limit(4)).all()

#         # return users.all()
#     return users


# def get_user_by_id(user_id: int):
#     with Session(engine) as session:
#         # user = session.exec(select(User).where(User.id == user_id)).first()
#         user = session.get(User, user_id)

#     return user


# def get_user_by_name():
#     with Session(engine) as session:
#         stmt = select(User).where(col(User.id).in_([33, 34, 35]))
#         user = session.exec(stmt).all()

#     return user


# def update_user_by_id(id: int, password: str):
#     with Session(engine) as session:
#         # user = session.get(User, id)
#         stmt = select(User).where(User.id == id)
#         user = session.exec(stmt).first()

#         if user is None:
#             return None  # FIXME: Можно было бы сделать исключение и обработать его в роутере, чтобы возвращать 404 статус

#         user.password_hash = password
#         session.add(user)
#         session.commit()

#         return user.username


# def delete_user(id: int):
#     with Session(engine) as session:
#         user = session.get(User, id)

#         session.delete(user)
#         session.commit()

#         return user


# def select_users_with_roles():
#     with Session(engine) as session:
#         # stmt = select(User, Role).where(User.role_id == Role.id)
#         # stmt = select(User, Role).join(Role)
#         stmt = select(User, Role).join(Role, isouter=True)
#         results = session.exec(stmt)

#         for user, role in results:
#             print(f"User: {user.username}, Role: {role.role}")


# def add_user_with_new_role():
#     with Session(engine) as session:

#         guest = Role(role="guest")

#         new_user = User(username="nobody", role=guest, password_hash="hash10")
#         session.add(new_user)
#         session.commit()


# def create_user_and_role():
#     with Session(engine) as session:
#         el_chupacabra = User(username="el_chupacabra", password_hash="hash11")
#         strangeer = User(username="strangeer", password_hash="hash12")

#         others = Role(role="others", users=[el_chupacabra, strangeer])

#         session.add(others)
#         session.commit()
#         session.refresh(others)

#         return True


# def select_users():
#     with Session(engine) as session:
#         stmt = select(User).where(User.username == "el_chupacabra")
#         users = session.exec(stmt).one()


# def get_users_role():
#     with Session(engine) as session:
#         stmt = select(User).where(User.username == "el_chupacabra")
#         result = session.exec(stmt).one()

#         return {"users role": result.role}


# def get_roles_members():
#     with Session(engine) as session:
#         stmt = select(Role).where(Role.role == "user")
#         result = session.exec(stmt).one()

#         return {"role members": result.users}
