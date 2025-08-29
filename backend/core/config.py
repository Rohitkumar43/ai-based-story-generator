#use the pydantic lib to handle env variable and the type safety
#AND TO MANGE ALLT HE CPRS AND THE CONFOIG FILE S


from pydantic_setting import BaseSettings
from Typing import list

from pydantic import filed_validators





class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    ALLOWED_ORIGIN :str = ""
    DEBUG:bool = True
    OPENAI_API_KEY:str = ""
    


@filed_validators()
def validate_database_url(cls, value:str) -> List[str]:
    return value.split(",") if value else []


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
    case_sensitive = False


settings = Settings()
    