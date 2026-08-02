from sqlalchemy import String, Float, DateTime, Integer, ForeignKey, func, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core.database import Base
from datetime import datetime
from enum import StrEnum
from models.contact import ContactModel


class DealStage(StrEnum):
    NEW = 'new'
    NEGOTIATION = 'negotiation'
    PROPOSAL = 'proposal'
    AT_WORK = 'at_work'
    COMEBACK = 'comeback'
    INSTALL = 'install'
    REJECT = 'reject'

class DealName(StrEnum):
    INTERNET_CONNECTION = 'internet_connection'
    VPN = 'VPN'
    TELEPHONE_SERVICE = 'telephone_service'
    MOBILE_SERVICE = 'mobile_service'
    SPECIAL_SERVICE = 'special_service'


class Deal(Base):
    __tablename__ = 'deals'

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    name : Mapped[DealName] = mapped_column(String(32), nullable=False)
    description : Mapped[str | None] = mapped_column(Text, nullable=True)
    amount : Mapped[Float | None] = mapped_column(Float, nullable=True, default=0)
    stage : Mapped[DealStage] = mapped_column(String(32), nullable=False, default=DealStage.NEW)
    contact_id : Mapped[int] = mapped_column(Integer, ForeignKey('contacts.id'), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now())
    contact :  Mapped[ContactModel] = relationship('ContactModel', back_populates='deals', lazy='selectin')
