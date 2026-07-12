from sqlmodel import SQLModel


class Post(SQLModel, table = True):
    pass