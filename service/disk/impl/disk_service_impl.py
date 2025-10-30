from fastapi import status
from utils.system.disk.disk_monitor import DiskMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from dto.response.disk.get_disk_usage_dto_response import GetDiskUsageDtoResponse
from service.disk.disk_service import DiskService
from config.decorators.measure_time import MeasureTime



class DiskServiceImpl(DiskService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- Disk 사용량 ---------------- #
    @MeasureTime()
    async def get_disk_usage(self) -> GetDiskUsageDtoResponse:
        """시스템 디스크 정보를 반환합니다."""


        try:
            # 필수 키 정의
            required_keys = {"total", "used", "free", "percent"}
            
            # 단위 변환 키 정의
            convert_keys = {"total", "used", "free"}

            # 디스크 정보 수집
            disk_value = await AsyncRunner.run_in_thread(func=DiskMonitor.disk_usage)

            # 전체 구조 검증
            if ValueValidator.is_valid_dict_structure(disk_value):
                raise ValueError("디스크 데이터가 비어있거나 형식이 올바르지 않습니다.")
            
            # 드라이브별 세부 검증 및 단위 변환 (Bytes → GB)
            for drive, info in disk_value.items():
                if ValueValidator.is_valid_dict(value=info, required_keys=required_keys):
                    raise ValueError(f"드라이브 {drive}의 데이터가 누락되었거나 유효하지 않습니다.")

                gb_fields = {
                    f"{k}_gb": round(info[k] / (1024 ** 3), 2)
                    for k in convert_keys
                    if k in info
                }

                disk_value[drive].update(gb_fields)

            # 정상 처리 상태 설정
            status_message = "정상적으로 처리되었습니다."
            status_code = status.HTTP_200_OK

        except ValueError as e:
            disk_value = {}
            status_message = str(e)
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        except Exception as e:
            disk_value = {}
            status_message = f"디스크 정보를 가져오는 중 오류가 발생했습니다: {e}"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return GetDiskUsageDtoResponse(
            disk_usage_values=disk_value,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )
