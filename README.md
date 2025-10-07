# Тестовое задание по написанию REST API

Решение выполнено на фреймворке FastAPI и базе Postgresql
с использованием SQLAlchemy ORM и Alembic миграций
Для запуска достаточно ввести команду:
```bash
docker compose up -d
```
Документация и проверка работы api доступна по адресу [http://localhost/docs](http://localhost/docs) после запуска контейнера
Отчёт о покрытии кода тестами находится в формате html в папке coverage_report(сгенерирован автоматически через pytest-cov)