import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///choices.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
