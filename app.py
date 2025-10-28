import uvicorn
from fastapi import FastAPI
from controller.system_controller import SystemController
from config.middleware.cors import CORS

app = FastAPI(title="시스템 API 목록") # /docs 접속
CORS.init_cors(app=app) # CORS 적용

# Controller 인스턴스 생성 및 라우터 등록
system_controller = SystemController()
app.include_router(router=system_controller.router, prefix="/system")


# 접속 URL: http://localhost:8000/api/./.
if __name__ == "__main__": 
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)