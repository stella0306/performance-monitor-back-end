from pydantic import BaseModel
from datetime import datetime

# 요청 양식
class GetCPUPercentDtoRequest(BaseModel):
    interval: float