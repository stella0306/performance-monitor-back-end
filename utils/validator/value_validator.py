class ValueValidator:
    """공통 데이터 유효성 검사 유틸리티"""

    @staticmethod
    def validate_on_off_value(value: str, field_name: str) -> str:
        """'on' 또는 'off' 유효성 검사"""
        
        value = str(value).strip().lower()
        
        if value not in {"on", "off"}:
            raise ValueError(f"{field_name}는 'on' 또는 'off'여야 합니다.")
        return value

    @staticmethod
    def is_valid_dict(value: dict, required_keys: set[str]) -> bool:
        """필수 키 존재 및 값 유효성 검증 (유효하면 True, 아니면 False)"""
        # value가 dict가 아니면 False
        if not isinstance(value, dict):
            return False

        # 필수 키 누락 여부 확인
        if not all(k in value for k in required_keys):
            return False

        # None 값 존재 여부 확인
        if any(v is None for v in value.values()):
            return False

        # 모든 조건을 통과하면 유효한 딕셔너리
        return True

    @staticmethod
    def is_valid_dict_structure(value: dict) -> bool:
        """딕셔너리 구조 자체가 유효한지 검사 (유효하면 True, 아니면 False)"""
        #  value가 dict가 아니면 False
        if not isinstance(value, dict):
            return False

        #  비어 있는지 검사
        if len(list(value.values())) == 0:
            return False

        # 위 조건을 모두 통과하면 유효한 딕셔너리
        return True
    

