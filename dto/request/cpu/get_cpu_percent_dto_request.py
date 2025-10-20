from pydantic import BaseModel

# 요청 양식
class GetCPUPercentDtoRequest(BaseModel):
    interval: float