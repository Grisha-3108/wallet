from uuid import UUID

from pydantic import (BaseModel,
                      ConfigDict)



class WalletSchema(BaseModel):
    id: UUID
    balance: float

    model_config = ConfigDict(from_attributes=True)