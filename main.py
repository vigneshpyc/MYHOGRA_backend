from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.V1.router import api_router
app = FastAPI()
origins = [
    # "http://localhost:5173",   # Vite dev server
    # "http://127.0.0.1:5173"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 🔥 REQUIRED for cookies (refresh token)
    allow_methods=["*"],      # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],      # Allow all headers (Authorization, etc.)
)
app.include_router(api_router, prefix='/api/V1')