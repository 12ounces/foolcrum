from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class ContactModel(Base):
    __tablename__ = 'contacts'

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name : Mapped[str] = mapped_column(String(False), nullable=False)
    inn : Mapped[str] = mapped_column(String(12), nullable=False)
    kpp : Mapped[str] = mapped_column(String(12), nullable=False)
    phone : Mapped[str] = mapped_column(String(10), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

