from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

# we will get the envronment variables here 
class Config(BaseSettings):
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )

AppConfig = Config()