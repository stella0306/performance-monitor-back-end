from pydantic import BaseModel

# 응답 양식, 오류 방지로 기본 값을 지정합니다.
class GetNetIoCountersDtoResponse(BaseModel):
    old_download_bytes: int = 0
    old_upload_bytes: int = 0
    new_download_bytes: int = 0
    new_upload_bytes: int = 0
    download_speed_mb: float = 0.0
    upload_speed_mb: float = 0.0
    network_measurement_time_delay: int = 0
    status_code: int = 0
    status_message: str = ""
    start_time: str = ""
    end_time: str = ""
    elapsed_time: str = ""