from app.core.config import AppConfig
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# we will create the database engine here 
app_database_engine = create_engine(
    url=AppConfig.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

# conneting with the database
def database_init():
    with app_database_engine.begin() as connection:
        yield connection

# we will create the database session here 
def app_session():
    
    Session  = sessionmaker(
        bind=app_database_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    
    with Session() as session:
        yield session