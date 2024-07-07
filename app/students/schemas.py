import typing as t

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from app.join_tables.models import StudentCourseJoin
from app.courses.schemas import CoursePublic


class StudentBase(SQLModel):
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    nacionality: str | None = Field(default=None, max_length=64)
    age: int | None = Field(default=None, ge=18, lt=90)
    is_active: bool = True


class StudentCreate(StudentBase):
    courses: list[CoursePublic] | None = Field(default=None)


class StudentUpdate(StudentBase):
    full_name: str | None = Field(max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class StudentPublic(StudentBase):
    id: int
    courses: list[CoursePublic]


class StudentList(SQLModel):
    data: list[StudentPublic]
    count: int

