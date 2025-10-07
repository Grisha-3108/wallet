import uuid
from decimal import Decimal

from sqlalchemy.types import UUID, Numeric
from sqlalchemy.orm import (Mapped, 
                            mapped_column)

from .base import Base


class Wallet(Base):
    __tablename__ = 'wallets'


    id: Mapped[uuid.UUID] = mapped_column(UUID,
                                          primary_key=True,
                                          default=uuid.uuid4)
    
    balance: Mapped[Decimal] = mapped_column(Numeric(10,2),
                                           nullable=False,
                                           default='0',
                                           server_default='0')