from fastapi import FastAPI
from app.middleware import setup_cors
from app.routes import router as api_router

app = FastAPI()

setup_cors(app)
app.include_router(api_router)
