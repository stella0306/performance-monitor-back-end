from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class CORS:
    
    @staticmethod
    def init_cors(app:FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )