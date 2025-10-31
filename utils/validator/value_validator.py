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
        """필수 키 존재 및 값 유효성 검증"""
        # value가 dict가 아니면 True
        if not isinstance(value, dict):
            return True
        
        # 필수 키가 하나라도 빠지면 True
        if not all(k in list(value.keys()) for k in required_keys):
            return True

        # 값이 None인 항목이 하나라도 있으면 True
        if any(v is None for v in list(value.values())):
            return True

        # 위 조건을 모두 통과하면 유효한 딕셔너리
        return False

    @staticmethod
    def is_valid_dict_structure(value: dict) -> bool:
        """딕셔너리 구조 자체가 유효한지 검사 (None 또는 비어있는 경우 False)"""
        #  value가 dict가 아니면 False
        if not isinstance(value, dict):
            return True

        #  비어 있는지 검사
        if len(list(value.values())) == 0:
            return True

        # 위 조건을 모두 통과하면 유효한 딕셔너리
        return False

