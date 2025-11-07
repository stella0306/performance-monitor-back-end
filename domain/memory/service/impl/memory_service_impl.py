from fastapi import status
from core.monitoring.memory_monitor import MemoryMonitor
from core.utils.validator.value_validator import ValueValidator
from core.utils.async_utils.async_runner import AsyncRunner
from domain.memory.dto.response.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse
from domain.memory.service.memory_service import MemoryService
from core.config.decorators.measure_time import MeasureTime


class MemoryServiceImpl(MemoryService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- 가상 메모리 ---------------- #
    @MeasureTime()
    async def get_virtual_memory(self) -> GetVirtualMemoryDtoResponse:
        """시스템 가상 메모리 정보를 반환합니다."""

        required_keys = {
            "memory_total_bytes",
            "memory_used_bytes",
            "memory_percent",
        }

        try:
            # 메모리 정보 수집
            memory_value = await AsyncRunner.run_in_thread(MemoryMonitor.get_virtual_memory)

            # 반환값 검증
            if not ValueValidator.is_valid_dict(value=memory_value, required_keys=required_keys):
                return GetVirtualMemoryDtoResponse(
                    memory_total_bytes=0.0,
                    memory_used_bytes=0.0,
                    memory_total_gb=0.0,
                    memory_used_gb=0.0,
                    memory_percent=0.0,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    status_message="메모리 데이터가 올바르지 않거나 일부 누락되었습니다.",
                    start_time="",
                    end_time="",
                    elapsed_time="",
                )

            # 정상 처리
            return GetVirtualMemoryDtoResponse(
                memory_total_bytes=memory_value["memory_total_bytes"],
                memory_used_bytes=memory_value["memory_used_bytes"],
                memory_total_gb=round(memory_value["memory_total_bytes"] / (1024 ** 3), 2),
                memory_used_gb=round(memory_value["memory_used_bytes"] / (1024 ** 3), 2),
                memory_percent=memory_value["memory_percent"],
                status_code=status.HTTP_200_OK,
                status_message="정상적으로 처리되었습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        except Exception:
            # 기타 예외 처리
            return GetVirtualMemoryDtoResponse(
                memory_total_bytes=0.0,
                memory_used_bytes=0.0,
                memory_total_gb=0.0,
                memory_used_gb=0.0,
                memory_percent=0.0,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="메모리 정보를 가져오는 중 오류가 발생했습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )