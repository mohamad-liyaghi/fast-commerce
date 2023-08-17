from fastapi import FastAPI
import uvicorn
from src.api import router

app = FastAPI(
    title='Fast Commerce',
    description='FastApi E-Commerce Project',
    version='1.0.0',
    docs_url='/',
    redoc_url='/redoc/'
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        host='0.0.0.0',
        app="main:app",
        reload=True,
        workers=1,
    )
