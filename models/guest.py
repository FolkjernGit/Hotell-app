from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from shortcuts import pkey, str_255


class Guest(Base):
    __tablename__ = "guests"
    id: Mapped[pkey]
    first_name: Mapped[str_255]
    last_name: Mapped[str_255]
    email: Mapped[str_255] = mapped_column(unique=True)
    
    def __repr__(self) -> str_255:
        return super().__repr__()
