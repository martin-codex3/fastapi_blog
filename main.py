from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteExceptions
from app.schemas.post_schemas import CreatePost, PostResponse
import random

app = FastAPI()
# we will load our static files here 
app.mount("/static", StaticFiles(directory = "static"), name="static")
templates = Jinja2Templates("templates")

posts = [
    {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "author": "Martin Banda",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python based on standard type hints.",
        "date_posted": "2026-06-01"
    },
    {
        "id": 2,
        "title": "Understanding EF Core Relationships",
        "author": "Martin Banda",
        "content": "One-to-many and many-to-many relationships in EF Core can be tricky when mixing Include() with Select().",
        "date_posted": "2026-06-15"
    },
    {
        "id": 3,
        "title": "Nuxt 4 and Tailwind CSS v4 Setup",
        "author": "Martin Banda",
        "content": "Configuring the @source directive correctly is key to getting Tailwind to scan your Nuxt 4 app directory.",
        "date_posted": "2026-07-02"
    },
    {
        "id": 4,
        "title": "Designing a Multi-Agent AI Pipeline",
        "author": "Martin Banda",
        "content": "Breaking down document analysis into specialized agents makes the system easier to test, debug, and extend.",
        "date_posted": "2026-07-03"
    },
    {
        "id": 5,
        "title": "Async Task Queues with Redis and arq",
        "author": "Martin Banda",
        "content": "Using arq with Redis provides a lightweight way to handle background jobs without the overhead of Celery.",
        "date_posted": "2026-07-04"
    },
    {
        "id": 6,
        "title": "Choosing a Storage Abstraction Layer",
        "author": "Martin Banda",
        "content": "A well-designed StorageService interface makes it painless to switch between local filesystem and MinIO backends.",
        "date_posted": "2026-07-05"
    },
    {
        "id": 7,
        "title": "JWT Authentication in ASP.NET Core",
        "author": "Martin Banda",
        "content": "Binding JWTSettings via IOptions and storing secrets with dotnet user-secrets keeps configuration clean and secure.",
        "date_posted": "2026-07-06"
    },
    {
        "id": 8,
        "title": "Building a Role-Based Permission System",
        "author": "Martin Banda",
        "content": "Seeding a 13-role permission structure upfront saves a lot of headaches later when access control needs grow.",
        "date_posted": "2026-07-07"
    }
]

@app.get("/", response_class = HTMLResponse, include_in_schema=False, name="home")
async def get_posts(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {"posts": posts, "title": "home"}
    )

# getting a single post from the frontend 
@app.get("/post/{post_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request=request,
                name="post.html",
                context={"post": post, "title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# for the api 
@app.get("/api/posts", status_code=status.HTTP_200_OK, response_model=list[PostResponse])
async def get_all_posts():
    return posts

# getting a single post
@app.get("/api/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

# for create a post 
@app.post("/api/post", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: CreatePost):

    new_post = {

        "id": 9,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "date_posted": "2026-07-07"
    }

    posts.append(new_post)
    return new_post


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