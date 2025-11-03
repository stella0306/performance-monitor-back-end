from pydantic import BaseModel

# 요청 양식
class GetCPUCountDtoRequest(BaseModel):
    logical_state: str = "off"