from abc import ABC, abstractmethod
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.request.cpu.get_cpu_count_dto_request import GetCPUCountDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from dto.response.cpu.get_cpu_count_dto_response import GetCPUCountDtoResponse
from dto.response.memory.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse

# 시스템 기능 추상화 작업입니다.

class SystemService(ABC):
    @abstractmethod
    async def get_cpu_percent(getCPUPercentDtoRequest: GetCPUPercentDtoRequest) -> GetCPUPercentDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass

    @abstractmethod
    async def get_cpu_count(getCPUCountDtoRequest: GetCPUCountDtoRequest) -> GetCPUCountDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass

    @abstractmethod
    async def get_virtual_memory() -> GetVirtualMemoryDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass
    