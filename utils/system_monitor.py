import psutil

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class SystemMonitor:
    # CPU 사용률을 가져오는 메서드
    @staticmethod
    def get_cpu_percent(interval: float | None, percpu: bool) -> float | list[float] | None:
        # interval: 측정 간격 (초). None이면 non-blocking 모드
        # percpu: True면 코어별, False면 전체 평균
        try:
            return psutil.cpu_percent(interval=interval, percpu=percpu)
        
        except Exception:
            # psutil 내부 오류나 시스템 접근 실패
            return None

    # CPU 코어 개수를 가져오는 메서드
    @staticmethod
    def get_cpu_count(logical: bool) -> int | None:
        # logical: True면 논리 코어 포함, False면 물리 코어만
        try:
            return psutil.cpu_count(logical=logical)

        except Exception:
            # psutil 내부 오류
            return None

    # 메모리 사용량을 가져오는 메서드
    @staticmethod
    def get_virtual_memory() -> dict | None:
        # 전체 메모리, 사용량, 사용률 등을 반환
        try:
            mem = psutil.virtual_memory()
            return {
                "memory_total_bytes": mem.total,
                "memory_used_bytes": mem.used,
                "memory_percent": mem.percent,
            }
        
        except Exception:
            # psutil 내부 오류
            return None


    # 네트워크 사용량을 가져오는 메서드
    @staticmethod
    def get_net_io_counters(pernic:bool=False, nowrap:bool=False) -> dict | None: # 일단은 파라미터 옵션을 만들었지만 외부에서 사용하지는 않을 것 입니다.
        try:
            # 네트워크 사용량 기록
            network = psutil.net_io_counters(pernic=pernic, nowrap=nowrap)
            return {
                "download_bytes": network.bytes_recv, # 다운로드
                "upload_bytes": network.bytes_sent, # 업로드
            }
        
        except Exception:
            return None