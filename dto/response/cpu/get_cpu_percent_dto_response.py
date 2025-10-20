from pydantic import BaseModel
from datetime import datetime

# 응답 양식
class GetCPUPercentDtoResponse(BaseModel):
    cpu_percent: float
    interval: float
    status_code: int
    status_message: str