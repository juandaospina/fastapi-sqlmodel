from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class StudentBase(SQLModel):
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    nacionality: str | None = Field(default=None, max_length=64)
    age: int | None = Field(default=None, ge=18, lt=90)
    is_active: bool = True


class StudentUpdate(StudentBase):
    full_name: str | None = Field(max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class StudentPublic(StudentBase):
    id: int


class StudentList(SQLModel):
    data: list[StudentPublic]
    count: int

