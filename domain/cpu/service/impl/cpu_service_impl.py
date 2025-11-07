from fastapi import status
from core.monitoring.cpu_monitor import CPUMonitor
from core.utils.validator.value_validator import ValueValidator
from core.utils.async_utils.async_runner import AsyncRunner
from domain.cpu.dto.request.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from domain.cpu.dto.request.get_cpu_count_dto_request import GetCPUCountDtoRequest
from domain.cpu.dto.response.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from domain.cpu.dto.response.get_cpu_count_dto_response import GetCPUCountDtoResponse
from domain.cpu.service.cpu_service import CPUService
from core.config.decorators.measure_time import MeasureTime


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

        # 입력값 검증
        try:
            interval_state = ValueValidator.validate_on_off_value(
                value=getCPUPercentDtoRequest.interval_state, field_name="interval_state"
            )
            percpu_state = ValueValidator.validate_on_off_value(
                value=getCPUPercentDtoRequest.percpu_state, field_name="percpu_state"
            )
        except ValueError as e:
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

        try:
            # Blocking 모드
            if interval_state == "on":
                if getCPUPercentDtoRequest.interval < 0.1:
                    return GetCPUPercentDtoResponse(
                        cpu_percent=0.0,
                        interval=getCPUPercentDtoRequest.interval,
                        interval_state=interval_state,
                        percpu_state=percpu_state,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        status_message="interval은 0.1 이상이어야 합니다. (Blocking)",
                        start_time="",
                        end_time="",
                        elapsed_time="",
                    )

                cpu_value = await AsyncRunner.run_in_thread(
                    CPUMonitor.get_cpu_percent,
                    getCPUPercentDtoRequest.interval,
                    percpu_state == "on",
                )
                return GetCPUPercentDtoResponse(
                    cpu_percent=cpu_value,
                    interval=getCPUPercentDtoRequest.interval,
                    interval_state=interval_state,
                    percpu_state=percpu_state,
                    status_code=status.HTTP_200_OK,
                    status_message="정상적으로 처리되었습니다. (Blocking)",
                    start_time="",
                    end_time="",
                    elapsed_time="",
                )

            # Non-blocking 모드
            cpu_value = await AsyncRunner.run_in_thread(
                CPUMonitor.get_cpu_percent,
                None,
                percpu_state == "on",
            )
            return GetCPUPercentDtoResponse(
                cpu_percent=cpu_value,
                interval=getCPUPercentDtoRequest.interval,
                interval_state=interval_state,
                percpu_state=percpu_state,
                status_code=status.HTTP_200_OK,
                status_message="정상적으로 처리되었습니다. (Non-blocking)",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        except Exception:
            # 예외 처리
            return GetCPUPercentDtoResponse(
                cpu_percent=0.0,
                interval=getCPUPercentDtoRequest.interval,
                interval_state=interval_state,
                percpu_state=percpu_state,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="CPU 사용률을 가져오는 중 오류가 발생했습니다.",
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

        # 입력값 검증
        try:
            logical_state = ValueValidator.validate_on_off_value(
                value=getCPUCountDtoRequest.logical_state, field_name="logical_state"
            )
        except ValueError as e:
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
            cpu_count = await AsyncRunner.run_in_thread(CPUMonitor.get_cpu_count, include_logical)

            return GetCPUCountDtoResponse(
                cpu_count=cpu_count,
                logical_state=logical_state,
                status_code=status.HTTP_200_OK,
                status_message=f"정상적으로 처리되었습니다. (논리 코어 {'포함' if include_logical else '제외'})",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        except Exception:
            return GetCPUCountDtoResponse(
                cpu_count=0,
                logical_state=logical_state,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="CPU 코어 개수를 가져오는 중 오류가 발생했습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )