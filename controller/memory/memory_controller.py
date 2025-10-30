from fastapi import APIRouter, Query
from service.memory.impl.memory_service_impl import MemoryServiceImpl
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.request.cpu.get_cpu_count_dto_request import GetCPUCountDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from dto.response.cpu.get_cpu_count_dto_response import GetCPUCountDtoResponse
from fastapi.responses import JSONResponse

class MemoryController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.memory_service = MemoryServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/memory", tags=["api"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)
        self.router.get("/virtual_memory")(self.get_virtual_memory)

    # 실제 API 메서드 작성
    
    # 메모리 사용량을 반환 
    async def get_virtual_memory(
        self
        ) -> JSONResponse:
        

        # 서비스 계층 호출
        response_dto = await self.memory_service.get_virtual_memory()

        # status_code를 포함하여 JSON 응답 반환
        return JSONResponse(
            status_code=response_dto["status_code"],
            content=response_dto
        )