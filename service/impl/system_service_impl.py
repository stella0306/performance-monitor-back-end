import asyncio
from fastapi import status
from utils.system_monitor import SystemMonitor
from dto.request.cpu.get_cpu_percent_dto_request import GetCPUPercentDtoRequest
from dto.request.cpu.get_cpu_count_dto_request import GetCPUCountDtoRequest
from dto.response.cpu.get_cpu_percent_dto_response import GetCPUPercentDtoResponse
from dto.response.cpu.get_cpu_count_dto_response import GetCPUCountDtoResponse
from dto.response.memory.get_virtual_memory_dto_response import GetVirtualMemoryDtoResponse
from dto.response.network.get_net_io_counters_dto_response import GetNetIoCountersDtoDtoResponse
from service.system_service import SystemService
from config.decorators.measure_time import MeasureTime


class SystemServiceImpl(SystemService):
    """시스템 서비스 실제 구현 클래스"""

    async def _run_in_thread(self, func, *args):
        """비동기 스레드 실행 헬퍼"""
        return await asyncio.to_thread(func, *args)

    @staticmethod
    def _validate_on_off(value: str, field_name: str):
        """'on'/'off' 유효성 검사"""
        value = str(value).strip().lower()
        
        if value not in {"on", "off"}:
            raise ValueError(f"{field_name}는 'on' 또는 'off'여야 합니다.")
        return value

    # ---------------- CPU 사용률 ---------------- #
    @MeasureTime()
    async def get_cpu_percent(self, getCPUPercentDtoRequest: GetCPUPercentDtoRequest) -> GetCPUPercentDtoResponse:
        """
        CPU 사용률을 반환합니다.
        - interval_state: 'on' → blocking / 'off' → non-blocking
        - percpu_state: 'on' → 코어별 / 'off' → 전체 평균
        """
        try:
            # 입력값 유효성 검사
            interval_state = self._validate_on_off(getCPUPercentDtoRequest.interval_state, "interval_state")
            percpu_state = self._validate_on_off(getCPUPercentDtoRequest.percpu_state, "percpu_state")

        except ValueError as e:
            # 잘못된 입력 처리
            return GetCPUPercentDtoResponse(
                cpu_percent=0.0,
                interval=getCPUPercentDtoRequest.interval,
                interval_state=getCPUPercentDtoRequest.interval_state,
                percpu_state=getCPUPercentDtoRequest.percpu_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=str(e),
                start_time="",
                end_time="",
                elapsed_time="",
            )

        interval = getCPUPercentDtoRequest.interval
        cpu_value = 0.0
        status_message = ""
        status_code = status.HTTP_200_OK

        try:
            # Blocking 모드
            if interval_state == "on":
                if interval < 0.1:
                    raise ValueError("interval은 0.1 이상이어야 합니다. (Blocking)")
                
                cpu_value = await self._run_in_thread(SystemMonitor.get_cpu_percent, interval, percpu_state == "on")
                status_message = "정상적으로 처리되었습니다. (Blocking)"

            # Non-blocking 모드
            else:
                cpu_value = await self._run_in_thread(SystemMonitor.get_cpu_percent, None, percpu_state == "on")
                status_message = "정상적으로 처리되었습니다. (Non-blocking)"

        except ValueError as e:
            # 입력값 오류 처리
            status_message = str(e)
            status_code = status.HTTP_400_BAD_REQUEST

        except Exception:
            # 기타 예외 처리
            status_message = "CPU 사용률을 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # 결과 응답 반환
        return GetCPUPercentDtoResponse(
            cpu_percent=cpu_value,
            interval=interval,
            interval_state=interval_state,
            percpu_state=percpu_state,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )

    # ---------------- CPU 코어 수 ---------------- #
    @MeasureTime()
    async def get_cpu_count(self, getCPUCountDtoRequest: GetCPUCountDtoRequest) -> GetCPUCountDtoResponse:
        """
        CPU 코어 개수를 반환합니다.
        - logical_state: 'on' → 논리코어 포함 / 'off' → 제외
        """

        try:
            # 입력값 유효성 검사
            logical_state = self._validate_on_off(getCPUCountDtoRequest.logical_state, "logical_state")

        except ValueError as e:
            # 잘못된 입력 처리
            return GetCPUCountDtoResponse(
                cpu_count=0,
                logical_state=getCPUCountDtoRequest.logical_state,
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=str(e),
                start_time="",
                end_time="",
                elapsed_time="",
            )

        #  논리 코어 포함 여부 결정
        include_logical = logical_state == "on"
        cpu_count = await self._run_in_thread(SystemMonitor.get_cpu_count, include_logical)
        message = f"정상적으로 처리되었습니다. (논리 코어 {'포함' if include_logical else '제외'})"

        # 결과 반환
        return GetCPUCountDtoResponse(
            cpu_count=cpu_count,
            logical_state=logical_state,
            status_code=status.HTTP_200_OK,
            status_message=message,
            start_time="",
            end_time="",
            elapsed_time="",
        )

    # ---------------- 가상 메모리 ---------------- #
    @MeasureTime()
    async def get_virtual_memory(self) -> GetVirtualMemoryDtoResponse:
        """시스템 가상 메모리 정보를 반환합니다."""

        # 기본 구조 초기화
        memory_data = {
            "memory_total_bytes": 0.0,
            "memory_used_bytes": 0.0,
            "memory_total_gb": 0.0,
            "memory_used_gb": 0.0,
            "memory_percent": 0.0,
        }

        try:
            # 메모리 정보 수집
            memory_value = await self._run_in_thread(SystemMonitor.get_virtual_memory)

            # 반환값 검증
            if not isinstance(memory_value, dict) or not all(k in memory_value for k in memory_data):
                raise ValueError("메모리 데이터가 올바르지 않거나 일부 누락되었습니다.")
            
            # 정상 처리
            memory_data.update(memory_value)
            status_message = "정상적으로 처리되었습니다."
            status_code = status.HTTP_200_OK

        except ValueError as e:
            # 데이터 누락 / 형식 오류
            status_message = str(e)
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        except Exception:
            # 기타 예외 처리
            status_message = "메모리 정보를 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # 결과 응답 반환
        return GetVirtualMemoryDtoResponse(
            memory_total_bytes=memory_data["memory_total_bytes"],
            memory_used_bytes=memory_data["memory_used_bytes"],
            memory_total_gb=memory_data["memory_total_gb"],
            memory_used_gb=memory_data["memory_used_gb"],
            memory_percent=memory_data["memory_percent"],
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )
    
    # ---------------- 네트워크 사용량 ---------------- #
    @MeasureTime()
    async def get_net_io_counters(self) -> GetNetIoCountersDtoDtoResponse:
        """시스템 네트워크 사용량을 반환합니다."""

        # 기본 구조 초기화
        network_data = {
            "download_bytes",
            "upload_bytes"
        }

        # 네트워크 데이터 측정 지연 시간
        measurement_time_delay = 1

        try:
            # 네트워크 정보 수집
            old_network_value = await asyncio.to_thread(SystemMonitor.get_net_io_counters)
            await asyncio.sleep(delay=measurement_time_delay) # 차이 값 계산을 위해 1초 대기
            new_network_value = await asyncio.to_thread(SystemMonitor.get_net_io_counters)


            # 반환값 검증
            if not isinstance(old_network_value, dict) or not all(k in old_network_value for k in network_data):
                raise ValueError("네트워크 데이터가 올바르지 않거나 일부 누락되었습니다. - 1")
            
            if not isinstance(new_network_value, dict) or not all(k in new_network_value for k in network_data):
                raise ValueError("네트워크 데이터가 올바르지 않거나 일부 누락되었습니다. - 2")
            

            # 정상 처리
            status_message = "정상적으로 처리되었습니다."
            status_code = status.HTTP_200_OK

        except ValueError as e:
            # 데이터 누락 / 형식 오류
            status_message = str(e)
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        except Exception:
            # 기타 예외 처리
            status_message = "네트워크 정보를 가져오는 중 오류가 발생했습니다."
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


        # 결과 응답 반환, 네트워크 다운로드/업로드 값은 Impl에서 계산.
        return GetNetIoCountersDtoDtoResponse(
            old_download_bytes=old_network_value["download_bytes"],
            old_upload_bytes=old_network_value["upload_bytes"],
            new_download_bytes=new_network_value["download_bytes"],
            new_upload_bytes=new_network_value["upload_bytes"],
            download_speed_mb=round((new_network_value["download_bytes"] - old_network_value["download_bytes"]) / (1024 ** 2), 2), # MB/s
            upload_speed_mb=round((new_network_value["upload_bytes"] - old_network_value["upload_bytes"]) / (1024 ** 2), 2), # MB/s
            network_measurement_time_delay=measurement_time_delay,
            status_code=status_code,
            status_message=status_message,
            start_time="",
            end_time="",
            elapsed_time="",
        )