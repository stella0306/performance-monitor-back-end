import psutil

# 간단한 예외처리만 적용, 대부분의 예외처리는 impl에서 처리.

class NetworkMonitor:

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