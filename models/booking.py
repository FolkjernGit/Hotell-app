from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base import Base
from shortcuts import pkey, str_255


class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[pkey]


