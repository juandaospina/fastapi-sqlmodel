from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.courses.models import Course
from app.common.deps import DBDepends
from .schemas import StudentList, StudentPublic, StudentUpdate, StudentCreate
from .models import Student


router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/{id}", response_model=StudentPublic, status_code=200)
def get_student_by_id(id: int, db: DBDepends) -> StudentPublic:
    statement = select(Student).where(Student.id == id)
    student = db.exec(statement).first()

    if not student:
        raise HTTPException(
            status_code=404, 
            detail="The student with this id does not exist in the system"
        )
    
    return student


@router.get("/", response_model=StudentList, status_code=200)
def get_students(db: DBDepends):
    """
    Retrieve students.
    """
    count_statement = select(func.count()).select_from(Student)
    count = db.exec(count_statement).one()

    statement = select(Student)
    students = db.exec(statement).all()

    return StudentList(data=students, count=count)


@router.post("/", response_model=StudentPublic, status_code=201)
def create_student(db: DBDepends, data: StudentCreate) -> StudentPublic:
    """
    Create a new student.
    """
    try:
        courses = []
        for course in data.courses:
            course_statement = select(Course).where(Course.id == course.id)
            course_res = db.exec(course_statement).first()

            if course_res:
                courses.append(course_res)

        student = Student.model_validate(data, strict=True, 
                                         update={"courses": courses})
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")
    

@router.put("/{id}", status_code=204,
            responses={204: {"description": "Successful update"}})
def update_student(id: int, db: DBDepends, data: StudentUpdate) -> None:
    """
    Update a student.
    """
    statement = select(Student).where(Student.id == id)
    student = db.exec(statement).first()

    if student is None:
        raise HTTPException(
            status_code=404, 
            detail="The student with this id does not exist in the system"
        )
    
    student.sqlmodel_update(data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)


@router.delete("/{id}", status_code=204, 
               responses={204: {"description": "Successful delete"}})
def delete_student(id: int, db: DBDepends):
    """
    Delete a student.
    """
    student = get_student_by_id(id, db)
    db.delete(student)
    db.commit()