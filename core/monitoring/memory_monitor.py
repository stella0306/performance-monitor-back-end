import psutil
from core.utils.monitor.monitor_helper import MonitorHelper

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class MemoryMonitor:
    
    # 메모리 사용량을 가져오는 메서드
    @staticmethod
    def get_virtual_memory() -> dict[str, float] | None:
        # 전체 메모리, 사용량, 사용률 등을 반환
        memory = MonitorHelper.safe_call(psutil.virtual_memory)
        
        if not memory:
            return None
        
        return {
                "memory_total_bytes": memory.total,
                "memory_used_bytes": memory.used,
                "memory_percent": memory.percent,
            }