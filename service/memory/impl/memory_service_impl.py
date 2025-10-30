from fastapi import status
from utils.system.memory.memory_monitor import MemoryMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from dto.response.memory.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse
from service.memory.memory_service import MemoryService
from config.decorators.measure_time import MeasureTime


class MemoryServiceImpl(MemoryService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- 가상 메모리 ---------------- #
    @MeasureTime()
    async def get_virtual_memory(self) -> GetVirtualMemoryDtoResponse:
        """시스템 가상 메모리 정보를 반환합니다."""

        # 기본 구조 초기화
        required_keys = {
            "memory_total_bytes",
            "memory_used_bytes",
            "memory_total_gb",
            "memory_used_gb",
            "memory_percent"
        }

        try:
            # 메모리 정보 수집
            memory_value = await AsyncRunner.run_in_thread(func=MemoryMonitor.get_virtual_memory)

            # 반환값 검증
            if (
                ValueValidator.is_valid_dict(value=memory_value, required_keys=required_keys)
                ):

                raise ValueError("메모리 데이터가 올바르지 않거나 일부 누락되었습니다.")
            
            # 정상 처리
            status_message = "정상적으로 처리되었습니다."
            status_code = status.HTTP_200_OK

        except ValueError as e:
            # 데이터 누락 / 형식 오류
            memory_value = {}
            status_message = str(e)
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        except Exception:
            # 기타 예외 처리
            memory_value = {}
            status_message = "메모리 정보를 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # 결과 응답 반환 (안정성을 위해 get 메서드 사용)
        return GetVirtualMemoryDtoResponse(
            memory_total_bytes=memory_value.get("memory_total_bytes", 0.0),
            memory_used_bytes=memory_value.get("memory_used_bytes", 0.0),
            memory_total_gb=round(memory_value.get("memory_total_bytes", 0.0) / (1024 ** 3), 2),
            memory_used_gb=round(memory_value.get("memory_used_bytes", 0.0) / (1024 ** 3), 2),
            memory_percent=memory_value.get("memory_percent", 0.0),
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )
