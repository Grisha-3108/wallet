import uuid

from fastapi import (APIRouter,
                     status)

from core.schemas import (OperationSchema,
                          WalletSchema)
from core.crud import (get_wallet_by_id,
                       update_wallet_balance,
                       create_wallet)


v1_router = APIRouter(prefix='/v1', tags=['Wallet v1 api'])


@v1_router.post('/wallets/{WALLET_UUID}/operation')
async def update_balance_handler(WALLET_UUID: uuid.UUID, 
                         operation: OperationSchema):
    return await update_wallet_balance(operation,
                                       WALLET_UUID)
    

@v1_router.get('/wallets/{WALLET_UUID}',
               response_model=WalletSchema)
async def get_wallet_handler(WALLET_UUID: uuid.UUID):
    return await get_wallet_by_id(WALLET_UUID)


@v1_router.post('/wallets/create/{WALLET_UUID}',
                status_code=status.HTTP_201_CREATED)
async def create_wallet_handler(WALLET_UUID: uuid.UUID):
    return await create_wallet(WALLET_UUID)