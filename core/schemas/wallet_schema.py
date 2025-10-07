from uuid import UUID
from decimal import Decimal

from pydantic import (BaseModel,
                      ConfigDict)



class WalletSchema(BaseModel):
    id: UUID
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)