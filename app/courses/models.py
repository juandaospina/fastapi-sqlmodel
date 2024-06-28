from sqlmodel import Field

from .schemas import CourseBase


class Course(CourseBase, table=True):
    __tablename__ = "courses"
    id: int | None = Field(default=None, primary_key=True)