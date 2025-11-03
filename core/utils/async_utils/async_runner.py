import asyncio

class AsyncRunner:
    """비동기 실행 관련 유틸리티 클래스"""

    @staticmethod
    async def run_in_thread(func, *args):
        """
        지정된 함수를 별도의 스레드에서 비동기로 실행합니다.
        """
        return await asyncio.to_thread(func, *args)

    @staticmethod
    async def sleep_for(delay: float | int) -> None:
        """
        지정된 시간(초) 동안 비동기적으로 대기합니다.
        """
        await asyncio.sleep(delay)
