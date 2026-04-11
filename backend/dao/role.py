from sqlmodel import Session, select
from database import engine
from models.role import Role


def create_roles():
    admin = Role(role="admin")
    power = Role(role="power")
    user = Role(role="user")

    with Session(engine) as session:
        session.add(admin)
        session.add(power)
        session.add(user)

        session.commit()
