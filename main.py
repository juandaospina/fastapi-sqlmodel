from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select, func

from app.student.models import Student
from app.student.schemas import StudentList, StudentBase, StudentPublic, StudentUpdate
from app.common.deps import DBDepends


app = FastAPI(
    title="FastAPI - SQLModel"
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


@app.get("/students", tags=["Students"], response_model=StudentList)
def get_students(db: DBDepends):
    """
    Retrieve students.
    """
    count_statement = select(func.count()).select_from(Student)
    count = db.exec(count_statement).one()

    statement = select(Student)
    students = db.exec(statement).all()

    return StudentList(data=students, count=count)


@app.post("/students", tags=["Students"], response_model=StudentPublic)
def create_student(db: DBDepends, data: StudentBase):
    """
    Create a new student.
    """
    try:
        student = Student.model_validate(data, strict=True)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")
    

@app.put("/students/{id}", tags=["Students"], responses={204: {"description": "Update succesfully"}})
def update_student(id: int, db: DBDepends, data: StudentUpdate) -> None:
    statement = select(Student).where(Student.id == id)
    student = db.exec(statement).first()

    if student is None:
        raise HTTPException(
            status_code=404, 
            detail="The user with this id does not exist in the system"
        )
    
    student.sqlmodel_update(data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)