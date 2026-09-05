from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"; PARTIALLY_PAID = "PARTIALLY_PAID"; PAID = "PAID"; CANCELLED = "CANCELLED"

class PaymentMethod(str, Enum):
    CASH = "CASH"; CARD = "CARD"; UPI = "UPI"; BANK_TRANSFER = "BANK_TRANSFER"
