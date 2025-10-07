import multiprocessing
from asyncio import TaskGroup

import pytest
from fastapi import status

from core.schemas import (OperationSchema,
                          OperationType)

@pytest.mark.asyncio
async def test_create_wallet(test_client):
    response = await test_client.post('http://localhost:8000/api/v1/wallets/create/c05a7ab4-1f44-4214-976d-7e2479e13452')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == 'c05a7ab4-1f44-4214-976d-7e2479e13452'


@pytest.mark.asyncio
async def test_create_existing_wallet(test_client, single_wallet):
    response = await test_client.post('http://localhost:8000/api/v1/wallets/create/36440671-05ef-45e7-949d-ee0f534c5876')
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == 'Ошибка при создании кошелька. Кошелек с таким uuid уже есть в базе'


@pytest.mark.asyncio
async def test_get_wallet(test_client, single_wallet):
    response = await test_client.get('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5876')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == '36440671-05ef-45e7-949d-ee0f534c5876'


@pytest.mark.asyncio
async def test_get_not_existing_wallet(test_client, single_wallet):
    response = await test_client.get('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5870')
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == 'Ошибка при получении кошелька. Кошелек с таким uuid не существует в базе'


@pytest.mark.asyncio
async def test_deposit_operation(test_client, single_wallet):
    response = await test_client.get('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5876')
    assert response.status_code == status.HTTP_200_OK
    balance_before = response.json()['balance']
    response = await test_client.post('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5876/operation',
                                      json=OperationSchema(operation_type=OperationType.deposit,
                                                           amount=100.55).model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['balance'] == float(balance_before) + 100.55


@pytest.mark.asyncio
async def test_withdraw_operation(test_client, single_wallet):
    response = await test_client.get('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5876')
    assert response.status_code == status.HTTP_200_OK
    balance_before = response.json()['balance']
    response = await test_client.post('http://localhost:8000/api/v1/wallets/36440671-05ef-45e7-949d-ee0f534c5876/operation',
                                      json=OperationSchema(operation_type=OperationType.withdraw,
                                                           amount=100.55).model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['balance'] == float(balance_before) - 100.55