# Тестовое задание по написанию REST API

Решение выполнено на фреймворке FastAPI и базе Postgresql
с использованием SQLAlchemy ORM и Alembic для миграций.
Файлы миграций находятся в папке alembic/versions.
Для запуска достаточно ввести команду:
```bash
docker compose up -d
```
Документация и проверка работы api доступна по адресу [http://localhost/docs](http://localhost/docs) после запуска контейнера.


Отчёт о покрытии кода тестами находится в формате html в папке coverage_report (сгенерирован автоматически через pytest-cov). 
Для обеспечения безопасности параллельных запросов с финансовыми операциями в базе включен уровень изоляции транзакций SERIALIZABLE.


Также был реализован GraphQL API. Для того, чтобы получить кошелек, отправьте на endpoint /graphql запрос с заголовком 
Content-Type: application/json и телом запроса в формате json через библиотеку httpx, например, такой запрос:
```python
import httpx

response = httpx.post(
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

#А вот так можно получить результат в json
print(response.json())
```
Для создания кошелька используйте следующий запрос к GraphQL:
```python
import httpx

response = httpx.post(
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
#А так можно посмотреть на созданный кошелек
print(response.json())
```
Для выполнения операции DEPOSIT используйте следующий код:
```python
import httpx

response = httpx.post(
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
#А так можно посмотреть на полученный баланс кошелька
print(response.json())
```
Для выполнения операции WITHDRAW используйте следующий код:
```python
import httpx

response = httpx.post(
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
#А так можно посмотреть на полученный баланс кошелька
print(response.json())
```
Для форматирования и статической проверки кода был использован ruff