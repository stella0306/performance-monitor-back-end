import asyncio
from fastapi import status
from utils.system_monitor import SystemMonitor
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from service.system_service import SystemService

# 시스템 서비스 실제 기능을 구현하는 작업입니다.
class SystemServiceImpl(SystemService):
    async def get_cpu_percent(self, getCPUPercentDtoRequest: GetCPUPercentDtoRequest) -> GetCPUPercentDtoResponse:
        # 유효성 검증
        is_valid = True if getCPUPercentDtoRequest.interval >= 0.1 else False # True / False 판별
        status_message = "정상적으로 처리됐습니다." if is_valid else "interval은(는) 0.1 이상이어야 합니다."

        # 기본값 초기화
        cpu_value = 0.0
        status_code = status.HTTP_404_NOT_FOUND

        if is_valid is True:
            # psutil은 동기이므로 스레드로 비동기 처리
            result = await asyncio.to_thread(SystemMonitor.get_cpu_percent, getCPUPercentDtoRequest.interval)

            if result is not None:
                cpu_value = result
                status_code = status.HTTP_200_OK

        # 결과 반환
        return GetCPUPercentDtoResponse(
            cpu_percent=cpu_value,
            interval=getCPUPercentDtoRequest.interval,
            status_code=status_code,
            status_message=status_message
        )