from sqlalchemy.orm import Mapped, mapped_column
from base import Base
from shortcuts import pkey, str_255


class Guest(Base):
    __tablename__ = "guests"
    id: Mapped[pkey]
    first_name: Mapped[str_255]
    last_name: Mapped[str_255]
    email: Mapped[str_255] = mapped_column(unique=True)
    
