from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_credentials_file: str | None = None
    google_credentials_json_b64: str | None = None
    google_spreadsheet_id: str | None = None
    google_worksheet_name: str = "Expenses"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()