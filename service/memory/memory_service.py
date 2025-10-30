from abc import ABC, abstractmethod
from dto.response.memory.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse

# 시스템 기능 추상화 작업입니다.

class MemoryService(ABC):
    @abstractmethod
    async def get_virtual_memory() -> GetVirtualMemoryDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass
