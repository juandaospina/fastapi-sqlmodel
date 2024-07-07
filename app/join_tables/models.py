from sqlmodel import SQLModel, Field


class StudentCourseJoin(SQLModel, table=True):
    __tablename__ = "student_course"
    student_id: int | None = Field(
        default=None, 
        foreign_key="students.id", 
        primary_key=True
    )
    course_id: int | None = Field(
        default=None, 
        foreign_key="courses.id", 
        primary_key=True
    )