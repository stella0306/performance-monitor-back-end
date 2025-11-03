from fastapi import status
from utils.system.network.network_monitor import NetworkMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from domain.network.dto.response.get_net_io_counters_dto_response import GetNetIoCountersDtoResponse
from domain.network.service.network_service import NetworkService
from config.decorators.measure_time import MeasureTime


class NetworkServiceImpl(NetworkService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- 네트워크 사용량 ---------------- #
    @MeasureTime()
    async def get_net_io_counters(self) -> GetNetIoCountersDtoResponse:
        """시스템 네트워크 사용량을 반환합니다."""

        required_keys = {"download_bytes", "upload_bytes"}
        measurement_time_delay = 1

        try:
            # 네트워크 정보 수집
            old_network_value = await AsyncRunner.run_in_thread(NetworkMonitor.get_net_io_counters)
            await AsyncRunner.sleep_for(measurement_time_delay)
            new_network_value = await AsyncRunner.run_in_thread(NetworkMonitor.get_net_io_counters)

            # 반환값 검증
            if not (
                ValueValidator.is_valid_dict(value=old_network_value, required_keys=required_keys)
                and ValueValidator.is_valid_dict(value=new_network_value, required_keys=required_keys)
                ):
                # 잘못된 데이터라면 바로 리턴
                return GetNetIoCountersDtoResponse(
                    old_download_bytes=0,
                    old_upload_bytes=0,
                    new_download_bytes=0,
                    new_upload_bytes=0,
                    download_speed_mb=0.0,
                    upload_speed_mb=0.0,
                    network_measurement_time_delay=measurement_time_delay,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    status_message="네트워크 데이터가 올바르지 않거나 일부 누락되었습니다.",
                    start_time="",
                    end_time="",
                    elapsed_time="",
                )

            # 정상 처리
            return GetNetIoCountersDtoResponse(
                old_download_bytes=old_network_value["download_bytes"],
                old_upload_bytes=old_network_value["upload_bytes"],
                new_download_bytes=new_network_value["download_bytes"],
                new_upload_bytes=new_network_value["upload_bytes"],
                download_speed_mb=round((new_network_value["download_bytes"] - old_network_value["download_bytes"]) / (1024 ** 2), 2),
                upload_speed_mb=round((new_network_value["upload_bytes"] - old_network_value["upload_bytes"]) / (1024 ** 2), 2),
                network_measurement_time_delay=measurement_time_delay,
                status_code=status.HTTP_200_OK,
                status_message="정상적으로 처리되었습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )

        except Exception:
            # 모든 예외 상황 처리
            return GetNetIoCountersDtoResponse(
                old_download_bytes=0,
                old_upload_bytes=0,
                new_download_bytes=0,
                new_upload_bytes=0,
                download_speed_mb=0.0,
                upload_speed_mb=0.0,
                network_measurement_time_delay=measurement_time_delay,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="네트워크 정보를 가져오는 중 오류가 발생했습니다.",
                start_time="",
                end_time="",
                elapsed_time="",
            )
