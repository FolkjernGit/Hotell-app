from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Boolean
from models.mixin import TimestampMixin
from shortcuts import pkey, dec
from datetime import datetime, timedelta

class Invoice(TimestampMixin,Base):
    __tablename__ = "invoices"
    id: Mapped[pkey]
    amount: Mapped[dec]
    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
    paid: Mapped[bool] = mapped_column(Boolean)
    price_per_night: Mapped[dec]
    expired: Mapped[bool] = mapped_column(Boolean)
    
    def pay_invoice(self):
        self.paid = True
        
    def check_if_expired(self):
        if (datetime.now() - self.created_at) > timedelta(days=10):
            self.expired = True
