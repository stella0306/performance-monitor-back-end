from abc import ABC, abstractmethod
from dto.response.network.get_net_io_counters_dto_response import GetNetIoCountersDtoResponse

# 시스템 기능 추상화 작업입니다.

class NetworkService(ABC):
    @abstractmethod
    async def get_net_io_counters() -> GetNetIoCountersDtoResponse:
        # 추상 단계에서는 비워둡니다.
        pass
    