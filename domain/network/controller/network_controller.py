from fastapi import APIRouter, Query
from domain.network.service.impl.network_service_impl import NetworkServiceImpl
from fastapi.responses import JSONResponse

class NetworkController:
    def __init__(self):
        # 구현한 시스템 기능 가져오기
        self.network_service = NetworkServiceImpl()

        # 라우터 인스턴스 생성
        self.router = APIRouter(prefix="/network", tags=["api"])

        # 라우터에 메서드 등록 (Spring의 @GetMapping 같은 역할)
        self.router.get("/net_io_counters")(self.get_net_io_counters)

    # 네트워크 사용량을 반환 
    async def get_net_io_counters(self) -> JSONResponse:
        response = await self.network_service.get_net_io_counters()

        # status_code를 포함하여 JSON 응답 반환
        return JSONResponse(
            status_code=response["status_code"],
            content=response
        )