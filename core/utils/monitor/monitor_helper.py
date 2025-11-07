from typing import Any

class MonitorHelper:
    """안전하게 함수를 실행하기 위한 공통 베이스 클래스"""
    
    @staticmethod
    def safe_call(func, *args, **kwargs) -> Any | None:
        try:
            return func(*args, **kwargs)
        
        except Exception:
            return None