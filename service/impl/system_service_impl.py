import asyncio
from fastapi import status
from utils.system_monitor import SystemMonitor
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.request.cpu.get_cpu_count_dto_request import GetCPUCountDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from dto.response.cpu.get_cpu_count_dto_response import GetCPUCountDtoResponse
from dto.response.memory.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse
from service.system_service import SystemService
from config.decorators.measure_time import MeasureTime

# 시스템 서비스 실제 기능을 구현하는 작업입니다.
class SystemServiceImpl(SystemService):

    # 클래스형 함수의 실행 시간을 측정하는 데이코레이터 적용
    @MeasureTime()
    async def get_cpu_percent(
        self, getCPUPercentDtoRequest: GetCPUPercentDtoRequest
    ) -> GetCPUPercentDtoResponse:
        """
        CPU 사용률을 반환합니다.
        interval_state: 'on' → blocking / 'off' → non-blocking
        percpu_state: 'on' → 코어별 사용률 / 'off' → 전체 평균 사용률
        """

        # 기본 변수 초기화
        interval = getCPUPercentDtoRequest.interval
        interval_state = str(getCPUPercentDtoRequest.interval_state).strip().lower()
        percpu_state = str(getCPUPercentDtoRequest.percpu_state).strip().lower()

        cpu_value = 0.0
        status_message = "문제 발생"
        status_code = status.HTTP_404_NOT_FOUND

        # percpu_state 유효성 검사
        if percpu_state not in {"on", "off"}:
            return GetCPUPercentDtoResponse(
                cpu_percent=cpu_value,
                interval=interval,
                interval_state=interval_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message="percpu_state는 'on' 또는 'off'여야 합니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        # Blocking 모드
        if interval_state == "on":
            if interval >= 0.1:
                cpu_value = await asyncio.to_thread(
                    SystemMonitor.get_cpu_percent, interval, percpu_state == "on"
                )
                status_message = "정상적으로 처리되었습니다. (Blocking)"
                status_code = status.HTTP_200_OK

            else:
                status_message = "interval은 0.1 이상이어야 합니다. (Blocking)"
                status_code = status.HTTP_400_BAD_REQUEST

        # Non-blocking 모드
        elif interval_state == "off":
            cpu_value = await asyncio.to_thread(
                SystemMonitor.get_cpu_percent, None, percpu_state == "on"
            )
            status_message = "정상적으로 처리되었습니다. (Non-blocking)"
            status_code = status.HTTP_200_OK

        # 잘못된 interval_state
        else:
            status_message = "interval_state는 'on' 또는 'off'여야 합니다."
            status_code = status.HTTP_400_BAD_REQUEST

        # 결과 반환
        return GetCPUPercentDtoResponse(
            cpu_percent=cpu_value,
            interval=interval,
            interval_state=interval_state,
            percpu_state=percpu_state,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )
    

    # 클래스형 함수의 실행 시간을 측정하는 데이코레이터 적용
    @MeasureTime()
    async def get_cpu_count(
        self, getCPUCountDtoRequest: GetCPUCountDtoRequest
    ) -> GetCPUCountDtoResponse:
        """
        CPU 코어 개수를 반환합니다.
        logical_state: 'on' → 논리코어 포함 / 'off' → 논리 코어 포함 안 함
        """

        # 기본 변수 초기화
        logical_state = str(getCPUCountDtoRequest.logical_state).strip().lower()

        cpu_value = 0.0
        status_message = "문제 발생"
        status_code = status.HTTP_404_NOT_FOUND

        # percpu_state 유효성 검사
        if logical_state not in {"on", "off"}:
            return GetCPUCountDtoResponse(
                cpu_count=cpu_value,
                logical_state=logical_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message="logical_state는 'on' 또는 'off'여야 합니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        # 논리코어 포함 모드
        if logical_state == "on":
            cpu_value = await asyncio.to_thread(
                SystemMonitor.get_cpu_count, True
            )
            status_message = "정상적으로 처리되었습니다. (논리 코어 포함, ON)"
            status_code = status.HTTP_200_OK

        # 논리코어 포함 안 함 모드
        else:
            cpu_value = await asyncio.to_thread(
                SystemMonitor.get_cpu_count, False
            )
            status_message = "정상적으로 처리되었습니다. (논리 코어 포함 안 함, OFF)"
            status_code = status.HTTP_200_OK

        # 결과 반환
        return GetCPUCountDtoResponse(
            cpu_count=cpu_value,
            logical_state=logical_state,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )
    
    # 클래스형 함수의 실행 시간을 측정하는 데이코레이터 적용
    @MeasureTime()
    async def get_virtual_memory(
        self
    ) -> GetVirtualMemoryDtoResponse:

        # 기본 변수 초기화
        memory_data = {
            "memory_total_bytes": 0.0,
            "memory_used_bytes": 0.0,
            "memory_total_gb": 0.0,
            "memory_used_gb": 0.0,
            "memory_percent": 0.0,
        }

        status_message = "문제 발생"
        status_code = status.HTTP_404_NOT_FOUND

        memory_value = await asyncio.to_thread(
                SystemMonitor.get_virtual_memory
            )

        # 데이터 유효성 검사
        if isinstance(memory_value, dict) and all(key in memory_value for key in list(memory_data.keys())):
            memory_data.update(memory_value)
            status_message = "정상적으로 처리되었습니다."
            status_code = status.HTTP_200_OK

        else:
            status_message = "메모리 데이터가 올바르지 않거나 일부 누락되었습니다."
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # 결과 반환
        return GetVirtualMemoryDtoResponse(
            memory_total_bytes=memory_data["memory_total_bytes"],
            memory_used_bytes=memory_data["memory_used_bytes"],
            memory_total_gb=memory_data["memory_total_gb"],
            memory_used_gb=memory_data["memory_used_gb"],
            memory_percent=memory_data["memory_percent"],
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )