from sqlmodel import Field, Relationship

from .schemas import StudentBase
from app.join_tables.models import StudentCourseJoin
from app.courses.models import Course


class Student(StudentBase, table=True):
    __tablename__ = "students"
    id: int | None = Field(default=None, primary_key=True)
    courses: list[Course] = Relationship(link_model=StudentCourseJoin)

