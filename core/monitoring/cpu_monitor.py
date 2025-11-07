import psutil
from core.utils.monitor.monitor_helper import MonitorHelper

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class CPUMonitor:
    
    # CPU 사용률을 가져오는 메서드
    @staticmethod
    def get_cpu_percent(interval: float | None, percpu: bool) -> float | list[float] | None:
        # interval: 측정 간격 (초). None이면 non-blocking 모드
        # percpu: True면 코어별, False면 전체 평균
        return MonitorHelper.safe_call(psutil.cpu_percent, interval=interval, percpu=percpu)

    # CPU 코어 개수를 가져오는 메서드
    @staticmethod
    def get_cpu_count(logical: bool) -> int  | None:
        # logical: True면 논리 코어 포함, False면 물리 코어만
        return MonitorHelper.safe_call(psutil.cpu_count, logical=logical)