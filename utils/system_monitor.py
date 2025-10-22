import psutil

class SystemMonitor:
    # CPU 사용률을 가져오는 메서드
    @staticmethod
    def get_cpu_percent(interval: float | None, percpu: bool) -> float | list[float] | None:
        # interval: 측정 간격 (초). None이면 non-blocking 모드
        # percpu: True면 코어별, False면 전체 평균
        try:
            return psutil.cpu_percent(interval=interval, percpu=percpu)
        
        except ValueError:
            # 잘못된 interval 값
            return None
        
        except Exception:
            # psutil 내부 오류나 시스템 접근 실패
            return None

    # CPU 코어 개수를 가져오는 메서드
    @staticmethod
    def get_cpu_count(logical: bool) -> int | None:
        # logical: True면 논리 코어 포함, False면 물리 코어만
        try:
            count = psutil.cpu_count(logical=logical)

            if count is None:
                # psutil이 None을 반환한 경우
                return None
            
            return count
        
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
                "memory_total_gb": round(mem.total / (1024 ** 3), 2),
                "memory_used_gb": round(mem.used / (1024 ** 3), 2),
                "memory_percent": mem.percent,
            }
        
        except Exception:
            # psutil 내부 오류
            return None
