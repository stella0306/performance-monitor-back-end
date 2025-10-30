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
        return (
            isinstance(value, dict)
            and all(k in value for k in required_keys)
            and all(v is not None for v in value.values())
        )
