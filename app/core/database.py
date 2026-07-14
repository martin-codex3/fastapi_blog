from app.core.config import AppConfig
from sqlalchemy.ext.asyncio.engine import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# we will create the database engine here 
app_database_engine = AsyncEngine(
   create_async_engine (
       url=AppConfig.DATABASE_URL,
   )
)

# conneting with the database
async def database_init():
    with await app_database_engine.begin() as connection:
        yield connection

# we will create the database session here 
def app_session():
    
    Session  = sessionmaker(
        bind=app_database_engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession
    )
    
    with Session() as session:
        yield session