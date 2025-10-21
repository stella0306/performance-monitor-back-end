from pydantic import BaseModel

# 응답 양식, 오류 방지로 기본 값을 지정합니다.
class GetVirtualMemoryDtoResponse(BaseModel):
    memory_total_bytes: float = 0.0
    memory_used_bytes: float = 0.0
    memory_total_gb: float = 0.0
    memory_used_gb: float = 0.0
    memory_percent: float = 0.0
    status_code: int = 0
    status_message: str = ""
    start_time: str = ""
    end_time: str = ""
    elapsed_time: str = ""