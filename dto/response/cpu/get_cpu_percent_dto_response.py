from pydantic import BaseModel

# 응답 양식, 오류 방지로 기본 값을 지정합니다.
class GetCPUPercentDtoResponse(BaseModel):
    cpu_percent: float = 0.0
    interval: float = 0.0
    interval_state: str = "off"
    status_code: int = 0
    status_message: str = ""
    start_time: str = ""
    end_time: str = ""
    elapsed_time: str = ""