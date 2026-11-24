import os
class Config:
    def __init__(self, overrides=None):
        overrides = overrides or {}
        self.APP_ENV = overrides.get("APP_ENV", os.getenv("APP_ENV", "development"))
        self.LOG_LEVEL = overrides.get("LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO"))
        self.DATABASE_PATH = overrides.get("DATABASE_PATH", os.getenv("DATABASE_PATH", "hospital.db"))
        self.TESTING = overrides.get("TESTING", False)
