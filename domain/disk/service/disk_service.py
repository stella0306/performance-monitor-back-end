from abc import ABC, abstractmethod
from domain.disk.dto.response.get_disk_usage_dto_response import GetDiskUsageDtoResponse

# 시스템 기능 추상화 작업입니다.

class DiskService(ABC):
    @abstractmethod
    async def get_disk_usage() -> GetDiskUsageDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass