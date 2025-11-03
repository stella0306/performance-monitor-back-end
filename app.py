import uvicorn
from fastapi import FastAPI
from domain.cpu.controller.cpu_controller import CPUController
from domain.disk.controller.disk_controller import DiskController
from domain.memory.controller.memory_controller import MemoryController
from domain.network.controller.network_controller import NetworkController
from config.middleware.cors import CORS

app = FastAPI(title="시스템 API 목록")  # /docs 접속
CORS.init_cors(app=app)  # CORS 적용

# Controller 인스턴스 생성 및 라우터 등록
cpu_controller = CPUController()
memory_controller = MemoryController()
network_controller = NetworkController()
disk_controller = DiskController()

# 모두 동일한 prefix(/system)로 등록
app.include_router(router=cpu_controller.router, prefix="/system")
app.include_router(router=memory_controller.router, prefix="/system")
app.include_router(router=network_controller.router, prefix="/system")
app.include_router(router=disk_controller.router, prefix="/system")

# 접속 URL: http://localhost:8000/system/...
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
