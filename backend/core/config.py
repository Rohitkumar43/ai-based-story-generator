#use the pydantic lib to handle env variable and the type safety
#AND TO MANGE ALLT HE CPRS AND THE CONFOIG FILE S


from pydantic_settings import BaseSettings
from typing import List

from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    ALLOWED_ORIGIN: str = ""
    DEBUG:bool = True
    OPENAI_API_KEY :str = ""

    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        if isinstance(self.ALLOWED_ORIGIN, str):
            return [i.strip() for i in self.ALLOWED_ORIGIN.split(',')]
        return self.ALLOWED_ORIGIN

    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = 'ignore'


settings = Settings()
    