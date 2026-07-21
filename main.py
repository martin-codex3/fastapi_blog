from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteExceptions
from contextlib import asynccontextmanager
from app.core.database import database_init
from app.controllers.posts.api.posts import posts_router
from app.controllers.users.api.users import users_router


# we will run the database here 
@asynccontextmanager
async def app_life_span(app: FastAPI):
    await database_init()
    yield
    print("shutting down server")

app_version = "v1"

app = FastAPI(
    lifespan=app_life_span,
    version=app_version
)

# we will load our static files here 
app.mount("/static", StaticFiles(directory = "static"), name="static")
templates = Jinja2Templates("templates")

# we will register the routes here 
app.include_router(
    router=posts_router,
    tags=["Posts Routes"],
    prefix="/api/posts"
)

app.include_router(
    router=users_router,
    tags=["Users Router"],
    prefix="/api/users"
)

# we will customize the errors here 
@app.exception_handler(StarletteExceptions)
async def general_exception_handler(request: Request, exception: StarletteExceptions):
    if exception.detail:
        message = (exception.detail)
    else:
        return "An error occured please check your request and try again"
    
    # we will check the request type here 
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": message}
        )
    
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exception.status_code,
            "message": message,
            "title": exception.status_code
        },
        status_code=exception.status_code
    )


# for the validation errors
@app.exception_handler(RequestValidationError)
async def validation_exeptions(request: Request, exceptions: RequestValidationError):

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "details": exceptions.errors
            }
        )
    
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Please check your request and try again!",
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )