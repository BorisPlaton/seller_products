from pathlib import Path

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    """
    Application settings. Most values are set from the environment
    variables.
    """
    BASE_DIR = Path(__file__).parent.parent
    ERRORS_LOG_FILE = BASE_DIR / 'logs' / 'errors.log'
    DEBUG_LOG_FILE = BASE_DIR / 'logs' / 'debug.log'

    HOST: str
    PORT: int
    DEBUG: bool

    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = Path(__file__).parent.parent.parent / '.env.dist'
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
