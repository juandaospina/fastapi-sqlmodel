from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.common.deps import DBDepends
from .schemas import CoursePublic, CourseList, CourseBase
from .models import Course


router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/", status_code=200, response_model=CourseList)
def get_courses(db: DBDepends):
    """
    Retrieve all courses.
    """
    count_statement = select(func.count()).select_from(Course)
    count = db.exec(count_statement).one()

    statement = select(Course) 
    courses = db.exec(statement).all()

    return CourseList(data=courses, count=count)


@router.post("/", status_code=201, response_model=CoursePublic)
def create_course(db: DBDepends, data: CourseBase):
    """
    Create a new course.
    """
    try:
        course = Course.model_validate(data, strict=True)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/{id}", status_code=200, response_model=CoursePublic)
def get_course_by_id(id: int, db: DBDepends):
    """
    Retrieve a one course by id
    """
    statement = select(Course).where(Course.id == id)
    course = db.exec(statement).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"The course with id {id} does not exist in the system"
        )
    
    return course