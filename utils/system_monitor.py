import psutil

class SystemMonitor:

    @staticmethod
    # cpu 사용률을 가져오는 메서드
    def get_cpu_percent(interval:float, percpu: bool) -> float | None:
        try:
            return psutil.cpu_percent(interval=interval, percpu=percpu)

        except Exception as e:
            return None

    # cpu 코어 개수를 가져오는 메서드
    @staticmethod
    def get_cpu_count(logical: bool) -> int | None:
        try:
            return psutil.cpu_count(logical=logical)
        
        except Exception as e:
            return None