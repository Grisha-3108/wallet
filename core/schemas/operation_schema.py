import enum

from pydantic import (BaseModel,
                      ConfigDict,
                      NonNegativeFloat)


class OperationType(enum.Enum):
    deposit = 'DEPOSIT'
    withdraw = 'WITHDRAW'



class OperationSchema(BaseModel):
    operation_type: OperationType
    amount: NonNegativeFloat

    model_config = ConfigDict(use_enum_values=True)