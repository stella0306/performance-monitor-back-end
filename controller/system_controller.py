from fastapi import APIRouter, Query
from service.impl.system_service_impl import SystemServiceImpl
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse

class SystemController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.system_service = SystemServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/cpu", tags=["cpu"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)
        self.router.get("/cpu_percent")(self.get_cpu_percent)

    # 실제 API 메서드 작성

    # 초 단위로 측정된 cpu 사용률의 평균 결과를 반환 
    async def get_cpu_percent(
            self, 
            interval: float = Query(default=0.5, description="CPU 측정 간격(초 단위)")
            ) -> GetCPUPercentDtoResponse:
        
        return await self.system_service.get_cpu_percent(
            getCPUPercentDtoRequest=GetCPUPercentDtoRequest(interval=interval)
        )