from sqlmodel import Field

from .schemas import StudentBase


class Student(StudentBase, table=True):
    __tablename__ = "students"
    id: int | None = Field(default=None, primary_key=True)


# class Course(SQLModel, table=True):
#     __tablename__ = "courses"
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(max_length=255, unique=True)
#     description: str | None = Field(default=None, max_length=255)
