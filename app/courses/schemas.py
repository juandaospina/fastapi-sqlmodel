from sqlmodel import SQLModel, Field, Relationship

# from app.join_tables.models import StudentCourseJoin


class CourseBase(SQLModel):
    name: str = Field(max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=255)
    # students: list["Student"] = Relationship(link_model=StudentCourseJoin, back_populates="courses")


class CourseUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class CoursePublic(CourseBase):
    id: int


class CourseList(SQLModel):
    data: list[CoursePublic]
    count: int