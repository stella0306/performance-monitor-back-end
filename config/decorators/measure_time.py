import functools
from datetime import datetime
from typing import Callable, Awaitable

# 클래스형 데이코레이터 적용
# 함수의 실행 시간을 측정합니다.

# ISO8601 변환을 방지하기 위해 datetime을 str타입으로 변경합니다.
class MeasureTime:
    def __call__(self, func: Callable[..., Awaitable]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = datetime.now()
            result = await func(*args, **kwargs)
            end = datetime.now()

            # 보기 좋은 문자열 포맷
            fmt = "%Y-%m-%d - %H:%M:%S.%f"
            start_fmt = start.strftime(fmt)[:-3]
            end_fmt = end.strftime(fmt)[:-3]

            # 실행 시간(초)
            elapsed = (end - start).total_seconds()

            data = result.model_dump() # 메서드 호출로 변경 가능한 딕셔너리 타입으로 변경
            data.update({
                "start_time": str(start_fmt),
                "end_time": str(end_fmt),
                "elapsed_time": str(elapsed)
            })
            # 결과 반환
            return data
        
        return wrapper