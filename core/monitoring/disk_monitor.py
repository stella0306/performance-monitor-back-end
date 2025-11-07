import psutil
from core.utils.monitor.monitor_helper import MonitorHelper

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class DiskMonitor:
    
    # 디스크 사용량을 가져오는 메서드
    @staticmethod
    def disk_usage() -> dict[str, dict[str, float]] | None:
        result = {}
        partitions = MonitorHelper.safe_call(psutil.disk_partitions)
        
        if not partitions:
            return None

        for part in partitions:
            usage = MonitorHelper.safe_call(psutil.disk_usage, part.mountpoint)
            
            if not usage:
                continue
            
            # 키 순서를 명확히 정의한 초기 딕셔너리 생성 (모든 초기값은 0으로 지정)
            # 마운트 포인트를 key로 저장
            result[part.mountpoint] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "total_gb": 0,
                "used_gb": 0,
                "free_gb": 0,
                "percent": usage.percent
            }
        
        return result or None