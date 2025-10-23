import psutil
import time
from pprint import pprint

# 코드 테스트 공간

# a = psutil.cpu_percent(interval=0.1, percpu=False)
# print(a)

# b = psutil.cpu_count(logical=True)
# print(b)

# c = psutil.virtual_memory()
# print(c)


# for process in psutil.process_iter(['pid', 'name']):
#     try:

#         p = psutil.Process(pid=process.info['pid'])
#         pprint(f"{process.info['name']}: {process.info['pid']} : {p}\n")
    
#     except TypeError:
#         pass

# while True:
#     pid = os.getpid()
#     t = psutil.Process()
#     print(t, pid)


# 네트워크 입출력 정보 (송신, 수신 바이트 등)
network = psutil.net_io_counters()

# print(f"보낸 데이터: {network.bytes_sent / (1024 ** 2):.2f} MB")
# print(f"받은 데이터: {network.bytes_recv / (1024 ** 2):.2f} MB")

def get_net_io_counters(pernic:bool=False, nowrap:bool=False): # 일단은 파라미터 옵션을 만들지만 외부에서 사용하지는 않을 것 입니다.
    try:
        # 네트워크 사용량 기록
        old_value = psutil.net_io_counters(pernic=pernic, nowrap=nowrap)
        print(old_value)
        old_recv = old_value.bytes_recv # 다운로드
        old_sent = old_value.bytes_sent # 업로드
        
        measurement_time_latency = 1
        time.sleep(measurement_time_latency) # 비동기적으로 1초 대기
        
        # 1초 기다렸다가 네트워크 사용량 기록
        new_value = psutil.net_io_counters()
        new_recv = new_value.bytes_recv # 다운로드
        new_sent = new_value.bytes_sent # 업로드
        
        # 네트워크 사용량 계산
        download_speed = (new_recv - old_recv) / (1024 ** 2)  # MB/s
        upload_speed = (new_sent - old_sent) / (1024 ** 2)    # MB/s
        
        return {
            "old_download_bytes": old_recv,
            "old_upload_bytes": old_sent,
            "new_download_bytes": new_recv,
            "new_upload_bytes": new_sent,
            "download_speed_mb": download_speed,
            "upload_speed_mb": upload_speed,
            "network_measurement_time_latency": measurement_time_latency

        }
    
    except Exception:
        return None

if __name__ == "__main__":
    print("실시간 네트워크 속도 (MB/s)")
    while True:
        result = get_net_io_counters(False, False)
        pprint(result)
        break


# 디스크 사용량 (C, D 드라이브 등을 시스템이 찾아냄)
# partitions = psutil.disk_partitions()

# for p in partitions:
#     usage = psutil.disk_usage(path=p.mountpoint)
#     print(f"{p.device} - {usage.percent}% 사용 중 ({usage.used / (1024 ** 3):.2f}GB / {usage.total / (1024 ** 3):.2f}GB)")