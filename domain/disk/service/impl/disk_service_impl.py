from fastapi import status
from utils.system.disk.disk_monitor import DiskMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from domain.disk.dto.response.get_disk_usage_dto_response import GetDiskUsageDtoResponse
from domain.disk.service.disk_service import DiskService
from config.decorators.measure_time import MeasureTime


class DiskServiceImpl(DiskService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- Disk 사용량 ---------------- #
    @MeasureTime()
    async def get_disk_usage(self) -> GetDiskUsageDtoResponse:
        """시스템 디스크 정보를 반환합니다."""

        required_keys = {"total", "used", "free", "percent"}
        convert_keys = {"total", "used", "free"}

        try:
            # 디스크 정보 수집
            disk_value = await AsyncRunner.run_in_thread(DiskMonitor.disk_usage)

            # 전체 구조 검증
            if not ValueValidator.is_valid_dict_structure(value=disk_value):
                return GetDiskUsageDtoResponse(
                    disk_usage_values={},
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    status_message="디스크 데이터가 비어있거나 형식이 올바르지 않습니다.",
                    start_time="",
                    end_time="",
                    elapsed_time="",
                )

            # 드라이브별 검증 및 단위 변환
            for drive, info in disk_value.items():
                if not ValueValidator.is_valid_dict(value=info, required_keys=required_keys):
                    return GetDiskUsageDtoResponse(
                        disk_usage_values={},
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        status_message=f"드라이브 {drive}의 데이터가 누락되었거나 유효하지 않습니다.",
                        start_time="",
                        end_time="",
                        elapsed_time="",
                    )
                    
                # Bytes → GB 변환
                for key in convert_keys:
                    if key in info:
                        info[f"{key}_gb"] = round(info[key] / (1024 ** 3), 2)

            # 정상 처리
            return GetDiskUsageDtoResponse(
                disk_usage_values=disk_value,
                status_code=status.HTTP_200_OK,
                status_message="정상적으로 처리되었습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        except Exception as e:
            # 예외 발생 시 바로 반환
            return GetDiskUsageDtoResponse(
                disk_usage_values={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message=f"디스크 정보를 가져오는 중 오류가 발생했습니다: {e}",
                start_time="",
                end_time="",
                elapsed_time="",
            )