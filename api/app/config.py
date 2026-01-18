from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_title: str = "Jailbreak Shield"
    api_version: str = "2.0.0"
    anthropic_api_key: str | None = None
    layer2_enabled: bool = True
    layer2_threshold: float = 0.5
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
