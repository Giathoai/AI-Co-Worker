import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Edtronaut AI Co-Worker Engine"
    VERSION: str = "1.0.0"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

settings = Settings()

if not settings.GOOGLE_API_KEY:
    print("Not Found API KEY")