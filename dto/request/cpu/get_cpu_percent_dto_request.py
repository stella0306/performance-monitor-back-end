from pydantic import BaseModel

# 요청 양식
class GetCPUPercentDtoRequest(BaseModel):
    interval: float = 1.0
    interval_state: str = "off"
    percpu_state: str = "off"