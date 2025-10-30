import psutil

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class DiskMonitor:
    @staticmethod
    def disk_usage():
        try:
            data = {}
            
            # 디스크 사용량 (C, D 드라이브 등을 찾아냄)
            partitions = psutil.disk_partitions()

            # 모든 디스크의 사용률 등을 반환
            for p in partitions:
                for k, v in psutil.disk_usage(path=p.mountpoint)._asdict().items():
                    # 드라이브 명으로 딕셔너리 생성
                    if p.mountpoint not in data:
                        # 키 순서 유지를 위해 초기화
                        data[p.mountpoint] = {
                            "total": 0,
                            "used": 0,
                            "free": 0,
                            "total_gb": 0,
                            "used_gb": 0,
                            "free_gb": 0,
                            "percent": 0,
                        }

                    # 업데이트
                    data[p.mountpoint][k] = v
                            
            return data
        
        except Exception:
            return None