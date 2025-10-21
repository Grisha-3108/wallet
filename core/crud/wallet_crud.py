from typing import AsyncGenerator
import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from core.database import async_session_factory
from core.schemas import OperationType, OperationSchema
from core.models import Wallet
from logger_config import logger


async def update_wallet_balance(
    operation: OperationSchema,
    id: uuid.UUID,
    session_factory: AsyncGenerator[AsyncSession] = async_session_factory,
) -> Wallet:
    async with session_factory() as session:
        try:
            wallet_to_update: Wallet = await session.get(Wallet, str(id))
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
        except StaleDataError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Ошибка при выполнении операции. '
                                'Повторите операцию позже.')
        except Exception:
            await session.rollback()
            logger.exception("Ошибка при изменении баланса кошелька.")


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
    async with session_factory() as session:
        try:
            new_wallet = Wallet(id=id, balance=0)
            session.add(new_wallet)
            await session.commit()
            return new_wallet
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка при создании кошелька. Кошелек с таким uuid уже есть в базе",
            )
        except Exception:
            await session.rollback()
            logger.exception("Ошибка при создании нового кошелька.")
