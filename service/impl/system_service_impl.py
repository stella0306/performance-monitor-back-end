import asyncio
from fastapi import status
from utils.system_monitor import SystemMonitor
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from service.system_service import SystemService
from config.decorators.measure_time import MeasureTime

# 시스템 서비스 실제 기능을 구현하는 작업입니다.
class SystemServiceImpl(SystemService):

    # 클래스형 함수의 실행 시간을 측정하는 데이코레이터 적용
    @MeasureTime()
    async def get_cpu_percent(self, getCPUPercentDtoRequest: GetCPUPercentDtoRequest) -> GetCPUPercentDtoResponse:

        # 기본값 초기화
        cpu_value = 0.0
        status_message = "문제 발생"
        status_code = status.HTTP_404_NOT_FOUND
        interval = getCPUPercentDtoRequest.interval
        interval_state = str(getCPUPercentDtoRequest.interval_state).strip().lower()

        # Blocking 모드
        if interval_state == "on":
            if interval >= 0.1:
                cpu_value = await asyncio.to_thread(SystemMonitor.get_cpu_percent, interval)
                status_message = "정상적으로 처리되었습니다. (Blocking)"
                status_code = status.HTTP_200_OK

            else:
                status_message = "interval는 '0.1'같거나 커야 합니다. (Blocking)"

        # Non-blocking 모드
        elif interval_state == "off":
            cpu_value = await asyncio.to_thread(SystemMonitor.get_cpu_percent, None)
            status_message = "정상적으로 처리되었습니다. (Non-blocking)"
            status_code = status.HTTP_200_OK

        else:
            status_message = "interval_mod는 'on' 또는 'off'여야 합니다."

        # 결과 반환
        # start_time, end_time, elapsed_time 파라미터는 MeasureTime 데코레이터에서 업데이트 됨
        return GetCPUPercentDtoResponse(
            cpu_percent=cpu_value,
            interval=interval,
            interval_state=interval_state,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time=""
        )