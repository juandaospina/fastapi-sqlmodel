from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.student.router import router as student_router


app = FastAPI(
    title="FastAPI - SQLModel"
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


# Api routes
app.include_router(student_router)