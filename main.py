from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.students.router import router as student_router
from app.courses.router import router as courses_route


app = FastAPI(
    title="FastAPI - SQLModel"
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


# Api routes
app.include_router(student_router)
app.include_router(courses_route)