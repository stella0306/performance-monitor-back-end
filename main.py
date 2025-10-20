import psutil

# 코드 테스트 공간

a = psutil.cpu_percent(interval=0.1, percpu=True)
print(a)