import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_wallet_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """query {
            wallet(id: "36440671-05ef-45e7-949d-ee0f534c5876") {
            id,
            balance
            }
        }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["wallet"]["id"]
        == "36440671-05ef-45e7-949d-ee0f534c5876"
    )


@pytest.mark.asyncio
async def test_get_not_existing_wallet_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """query {
            wallet(id: "36440671-05ef-45e7-949d-ee0f534c5875") {
            id,
            balance
            }
        }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == None
    assert response.json().get("errors")


@pytest.mark.asyncio
async def test_create_wallet_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """mutation {
            createNewWallet(id: "36440671-05ef-45e7-949d-ee0f534c5878"){
            id,
            balance
                }
                    }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["createNewWallet"]["id"]
        == "36440671-05ef-45e7-949d-ee0f534c5878"
    )
    assert response.json()["data"]["createNewWallet"]["balance"] == 0


@pytest.mark.asyncio
async def test_create_already_existing_wallet_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """mutation {
            createNewWallet(id: "36440671-05ef-45e7-949d-ee0f534c5876"){
            id,
            balance
                }
                    }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == None
    assert (
        response.json()["errors"][0]["message"]
        == "409: Ошибка при создании кошелька. Кошелек с таким uuid уже есть в базе"
    )


@pytest.mark.asyncio
async def test_deposit_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """query {
            wallet(id: "36440671-05ef-45e7-949d-ee0f534c5876") {
            id,
            balance
            }
        }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    balance_before = response.json()["data"]["wallet"]["balance"]
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """mutation {
            deposit(id: "36440671-05ef-45e7-949d-ee0f534c5876", amount: 100){
            id,
            balance
                }
                    }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["deposit"]["balance"] == balance_before + 100


@pytest.mark.asyncio
async def test_deposit_graphql(test_client, single_wallet):
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """query {
            wallet(id: "36440671-05ef-45e7-949d-ee0f534c5876") {
            id,
            balance
            }
        }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    balance_before = response.json()["data"]["wallet"]["balance"]
    response = await test_client.post(
        "http://localhost:8000/graphql",
        json={
            "query": """mutation {
            withdraw(id: "36440671-05ef-45e7-949d-ee0f534c5876", amount: 100){
            id,
            balance
                }
                    }"""
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["withdraw"]["balance"] == balance_before - 100
