from fastapi import status
from utils.system.disk.disk_monitor import DiskMonitor
from utils.validator.value_validator import ValueValidator
from utils.async_utils.async_runner import AsyncRunner
from service.disk.disk_service import DiskService
from config.decorators.measure_time import MeasureTime


class DiskServiceImpl(DiskService):
    """시스템 서비스 실제 구현 클래스"""

    # ---------------- ? ---------------- #