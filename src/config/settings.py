import os
from pathlib import Path

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    BASE_DIR = Path(__file__).parent.parent
    HOST: str = os.getenv('HOST')
    PORT: int = os.getenv('PORT')
    DEBUG: bool = bool(os.getenv('DEBUG'))

    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ERRORS_LOG_FILE = BASE_DIR / 'logs' / 'errors.log'
    DEBUG_LOG_FILE = BASE_DIR / 'logs' / 'debug.log'

    class Config:
        env_file = map(
            lambda x: Path(__file__).parent.parent.parent / x, ['.env', '.env.dist']
        )
        env_file_encoding = 'utf-8'
        allow_mutation = False

    @property
    def postgres_url(self):
        """
        Returns a constructed URL to the Postgresql database.
        """
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = ProjectSettings()
