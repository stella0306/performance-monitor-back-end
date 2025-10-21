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
    
    # 메모리 사용량을 가져오는 메서드
    @staticmethod
    def get_virtual_memory() -> dict | None:
        try:
            mem = psutil.virtual_memory()
            return {
                "memory_total_bytes": mem.total,
                "memory_used_bytes": mem.used,
                "memory_total_gb": round(mem.total / (1024 ** 3), 2),
                "memory_used_gb": round(mem.used / (1024 ** 3), 2),
                "memory_percent": mem.percent
            }
        
        except Exception as e:
            return None