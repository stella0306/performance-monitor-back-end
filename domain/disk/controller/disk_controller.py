from fastapi import APIRouter, Query
from domain.disk.service.impl.disk_service_impl import DiskServiceImpl
from domain.disk.dto.response.get_disk_usage_dto_response import GetDiskUsageDtoResponse
from fastapi.responses import JSONResponse

class DiskController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.disk_service = DiskServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/disk", tags=["api"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)
        self.router.get("/disk_usage")(self.get_disk_usage)
        

    # 디스크 사용량을 반환 
    async def get_disk_usage(self) -> JSONResponse:
        response = await self.disk_service.get_disk_usage()

        # status_code를 포함하여 JSON 응답 반환
        return JSONResponse(
            status_code=response["status_code"],
            content=GetDiskUsageDtoResponse(**response).model_dump()
        )
