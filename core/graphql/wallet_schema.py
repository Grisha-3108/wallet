import uuid

import strawberry
from fastapi import HTTPException, status

from core.crud import get_wallet_by_id, create_wallet, update_wallet_balance
from core.schemas import OperationType, OperationSchema


class WalletSchema:
    id: uuid.UUID
    balance: float

    def __init__(self, id, balance):
        self.id = id
        self.balance = balance


@strawberry.type(name="WalletSchema")
class WalletType:
    id: strawberry.ID
    balance: float


@strawberry.type
class Query:
    @strawberry.field(graphql_type=WalletType)
    async def wallet(self, id: str) -> WalletSchema:
        wallet = await get_wallet_by_id(uuid.UUID(id))
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Кошелька с таким id не существует.",
            )
        return WalletSchema(id=wallet.id, balance=wallet.balance)


@strawberry.type
class Mutation:
    @strawberry.mutation(graphql_type=WalletType)
    async def create_new_wallet(self, id: str) -> WalletSchema:
        res = await create_wallet(uuid.UUID(id))
        return WalletSchema(id=res.id, balance=res.balance)

    @strawberry.mutation(graphql_type=WalletType)
    async def deposit(self, id: str, amount: float) -> WalletSchema:
        res = await update_wallet_balance(
            OperationSchema(operation_type=OperationType.deposit.value, amount=amount),
            uuid.UUID(id),
        )
        return WalletSchema(id=res.id, balance=res.balance)

    @strawberry.mutation(graphql_type=WalletType)
    async def withdraw(self, id: str, amount: float) -> WalletSchema:
        res = await update_wallet_balance(
            OperationSchema(operation_type=OperationType.withdraw.value, amount=amount),
            uuid.UUID(id),
        )
        return WalletSchema(id=res.id, balance=res.balance)


schema = strawberry.Schema(query=Query, mutation=Mutation)
