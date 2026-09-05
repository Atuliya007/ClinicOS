from enum import Enum

class AppointmentStatus(str, Enum):
    PENDING = "PENDING"; WAITING = "WAITING"; IN_PROCESS = "IN_PROCESS"; COMPLETED = "COMPLETED"; CANCELLED = "CANCELLED"; NO_SHOW = "NO_SHOW"
