from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API cho Hệ thống AI Co-Worker (Mô phỏng nhân sự Gucci) của Edtronaut."
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với Edtronaut AI Engine. Hãy truy cập /docs để xem tài liệu API."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)