from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base de datos
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # WhatsApp
    VERIFY_TOKEN: str
    WHATSAPP_TOKEN: str
    PHONE_NUMBER_ID: str

    # OpenRouter / LLM
    OPENROUTER_API_KEY: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }




settings = Settings()


def get_settings() -> Settings:
    return settings