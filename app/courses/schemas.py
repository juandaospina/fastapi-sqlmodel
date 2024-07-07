from sqlmodel import SQLModel, Field, Relationship


class CourseBase(SQLModel):
    name: str = Field(max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=255)


class CourseUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class CoursePublic(CourseBase):
    id: int


class CourseList(SQLModel):
    data: list[CoursePublic]
    count: int