import psutil

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class DiskMonitor:
    
    # 디스크 사용량을 가져오는 메서드
    @staticmethod
    def disk_usage():
        try:
            result = {}

            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    
                # 접근 권한이 없는 파티션은 건너뜀
                except PermissionError:
                    continue
                
                # 예상하지 못 한 파티션도 건너뜀
                except Exception:
                    continue

                # 키 순서를 명확히 정의한 초기 딕셔너리 생성
                data = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                    "total_gb": round(usage.total / 1024**3, 2),
                    "used_gb": round(usage.used / 1024**3, 2),
                    "free_gb": round(usage.free / 1024**3, 2),
                }

                # 마운트 포인트를 key로 저장
                result[part.mountpoint] = data

            return result

        except Exception:
            return None