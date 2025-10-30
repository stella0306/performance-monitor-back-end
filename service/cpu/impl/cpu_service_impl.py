import asyncio
from fastapi import status
from utils.system_monitor import SystemMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.request.cpu.get_cpu_count_dto_request import GetCPUCountDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from dto.response.cpu.get_cpu_count_dto_response import GetCPUCountDtoResponse
from service.cpu.cpu_service import CPUService
from config.decorators.measure_time import MeasureTime


class CPUServiceImpl(CPUService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- CPU 사용률 ---------------- #
    @MeasureTime()
    async def get_cpu_percent(self, getCPUPercentDtoRequest: GetCPUPercentDtoRequest) -> GetCPUPercentDtoResponse:
        """
        CPU 사용률을 반환합니다.
        - interval_state: 'on' → blocking / 'off' → non-blocking
        - percpu_state: 'on' → 코어별 / 'off' → 전체 평균
        """
        try:
            # 입력값 유효성 검사
            interval_state = ValueValidator.validate_on_off_value(value=getCPUPercentDtoRequest.interval_state, field_name="interval_state")
            percpu_state = ValueValidator.validate_on_off_value(value=getCPUPercentDtoRequest.percpu_state, field_name="percpu_state")

        except ValueError as e:
            # 잘못된 입력 처리
            return GetCPUPercentDtoResponse(
                cpu_percent=0.0,
                interval=getCPUPercentDtoRequest.interval,
                interval_state=getCPUPercentDtoRequest.interval_state,
                percpu_state=getCPUPercentDtoRequest.percpu_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=str(e),
                start_time="",
                end_time="",
                elapsed_time="",
            )

        interval = getCPUPercentDtoRequest.interval
        cpu_value = 0.0
        status_message = ""
        status_code = status.HTTP_200_OK

        try:
            # Blocking 모드
            if interval_state == "on":
                if interval < 0.1:
                    raise ValueError("interval은 0.1 이상이어야 합니다. (Blocking)")
                
                cpu_value = await AsyncRunner.run_in_thread(SystemMonitor.get_cpu_percent, interval, percpu_state == "on")
                status_message = "정상적으로 처리되었습니다. (Blocking)"

            # Non-blocking 모드
            else:
                cpu_value = await AsyncRunner.run_in_thread(SystemMonitor.get_cpu_percent, None, percpu_state == "on")
                status_message = "정상적으로 처리되었습니다. (Non-blocking)"

        except ValueError as e:
            # 입력값 오류 처리
            status_message = str(e)
            status_code = status.HTTP_400_BAD_REQUEST

        except Exception:
            # 기타 예외 처리
            status_message = "CPU 사용률을 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # 결과 응답 반환
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

    # ---------------- CPU 코어 수 ---------------- #
    @MeasureTime()
    async def get_cpu_count(self, getCPUCountDtoRequest: GetCPUCountDtoRequest) -> GetCPUCountDtoResponse:
        """
        CPU 코어 개수를 반환합니다.
        - logical_state: 'on' → 논리코어 포함 / 'off' → 제외
        """

        try:
            # 입력값 유효성 검사
            logical_state = ValueValidator.validate_on_off_value(value=getCPUCountDtoRequest.logical_state, field_name="logical_state")

        except ValueError as e:
            # 잘못된 입력 처리
            return GetCPUCountDtoResponse(
                cpu_count=0,
                logical_state=getCPUCountDtoRequest.logical_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=str(e),
                start_time="",
                end_time="",
                elapsed_time="",
            )

        try:
            # 논리 코어 포함 여부 결정
            include_logical = logical_state == "on"
            cpu_count = await AsyncRunner.run_in_thread(SystemMonitor.get_cpu_count, include_logical)
            status_message = f"정상적으로 처리되었습니다. (논리 코어 {'포함' if include_logical else '제외'})"
            status_code = status.HTTP_200_OK

        except Exception:
            # 기타 예외 처리
            status_message = "CPU 코어 개수를 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


        # 결과 반환
        return GetCPUCountDtoResponse(
            cpu_count=cpu_count,
            logical_state=logical_state,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )