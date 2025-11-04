from fastapi import APIRouter, Query
from domain.cpu.service.impl.cpu_service_impl import CPUServiceImpl
from domain.cpu.dto.request.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from domain.cpu.dto.request.get_cpu_count_dto_request import GetCPUCountDtoRequest
from domain.cpu.dto.response.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from domain.cpu.dto.response.get_cpu_count_dto_response import GetCPUCountDtoResponse
from fastapi.responses import JSONResponse
import json

class CPUController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.cpu_service = CPUServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/cpu", tags=["api"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)
        self.router.get("/cpu_percent")(self.get_cpu_percent)
        self.router.get("/cpu_count")(self.get_cpu_count)

    # 초 단위로 측정된 cpu 사용률의 평균 결과를 반환 
    async def get_cpu_percent(self, interval: float = Query(default=1), interval_state: str = Query(default="off"), percpu_state: str = Query(default="off")) -> JSONResponse:
        response = await self.cpu_service.get_cpu_percent(
            getCPUPercentDtoRequest=GetCPUPercentDtoRequest(
                interval=interval,
                interval_state=interval_state,
                percpu_state=percpu_state
            )
        )

        
        # status_code를 포함하여 JSON 응답 반환
        return JSONResponse(
            status_code=response["status_code"],
            content=GetCPUPercentDtoResponse(**response).model_dump()
        )
        

    # cpu 코어 개수를 반환 
    async def get_cpu_count(self, logical_state: str = Query(default="off")) -> JSONResponse:
        response = await self.cpu_service.get_cpu_count(
            getCPUCountDtoRequest=GetCPUCountDtoRequest(
                logical_state=logical_state
            )
        )

        # status_code를 포함하여 JSON 응답 반환
        return JSONResponse(
            status_code=response["status_code"],
            content=GetCPUCountDtoResponse(**response).model_dump()
        )