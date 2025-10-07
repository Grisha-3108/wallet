import enum
from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel, ConfigDict


class OperationType(enum.Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class OperationSchema(BaseModel):
    operation_type: OperationType
    amount: Annotated[float, Ge(ge=0)]

    model_config = ConfigDict(use_enum_values=True)
