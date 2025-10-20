import psutil
from datetime import datetime

class SystemMonitor:

    @staticmethod
    # cpu 사용률을 가져오는 메서드
    def get_cpu_percent(interval:float) -> float | None:
        try:
            return psutil.cpu_percent(interval=interval)

        except Exception as e:
            return None