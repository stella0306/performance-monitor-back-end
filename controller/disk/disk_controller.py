from fastapi import APIRouter, Query
from service.disk.impl.disk_service_impl import DiskServiceImpl
from fastapi.responses import JSONResponse

class DiskController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.disk_service = DiskServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/disk", tags=["api"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)

    # 실제 API 메서드 작성

