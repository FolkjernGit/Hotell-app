from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from datetime import datetime
from typing import Optional

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, onupdate=datetime.now())
    
class SoftDeletionMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean,default=False)
    
    def soft_delete(self):
        self.is_deleted  = True
    
    def restore(self):
        self.is_deleted = False