from typing import AsyncGenerator
import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.database import async_session_factory
from core.schemas import OperationType, OperationSchema
from core.models import Wallet


async def update_wallet_balance(
    operation: OperationSchema,
    id: uuid.UUID,
    session_factory: AsyncGenerator[AsyncSession] = async_session_factory,
) -> Wallet:
    try:
        async with session_factory() as session:
            wallet_to_update: Wallet = await session.get(Wallet, id)
            if not wallet_to_update:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ошибка при выполнении транзакции. "
                    "Кошелька с таким uuid не существует",
                )
            if operation.operation_type == OperationType.deposit.value:
                wallet_to_update.balance += Decimal(str(operation.amount))
            elif operation.operation_type == OperationType.withdraw.value:
                wallet_to_update.balance -= Decimal(str(operation.amount))
            await session.commit()
            return wallet_to_update
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ошибка при выполнении транзакции. Повторите операцию позже.",
        )


async def get_wallet_by_id(
    id: uuid.UUID, session_factory: AsyncGenerator[AsyncSession] = async_session_factory
) -> Wallet:
    async with session_factory() as session:
        result = await session.get(Wallet, id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка при получении кошелька. "
                "Кошелек с таким uuid не существует в базе",
            )
        return result


async def create_wallet(
    id: uuid.UUID = uuid.uuid4(),
    session_factory: AsyncGenerator[AsyncSession] = async_session_factory,
) -> Wallet:
    try:
        async with session_factory() as session:
            new_wallet = Wallet(id=id, balance=0)
            session.add(new_wallet)
            await session.commit()
            return new_wallet
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ошибка при создании кошелька. Кошелек с таким uuid уже есть в базе",
        )
