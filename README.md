# Tron Microservice

## Описание

Tron Microservice — это приложение, разработанное с использованием FastAPI, предназначенное для получения информации о кошельках Tron, включая баланс, пропускную способность и энергию, а также сохранение истоории запросов кошельков.

## Стек технологий
- **FastAPI**: веб-фреймворк для создания API.
- **SQLAlchemy**: ORM для работы с базой данных.
- **PostgreSQL**: реляционная база данных.
- **Alembic**: инструмент для миграции базы данных.
- **Pydantic**: библиотека для валидации данных.
- **Pytest**: библиотека для тестирования приложения.

---

## Установка

### Предварительные требования
- Python 3.8 или выше
- Docker и Docker Compose

### Клонирование репозитория
```bash
git clone https://github.com/skv43r/tron_microservice.git
cd tron_microservice
```

### Настройка окружения

1. Создайте файл `.env` в корне проекта и добавьте следующие переменные:
   ```dotenv
	MODE
	DB_HOST
	DB_PORT
	DB_USER
	DB_PASS
	DB_NAME
    DB_URL=postgresql+asyncpg://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}
	TEST_DB_HOST
	TEST_DB_PORT
	TEST_DB_USER
	TEST_DB_PASS
	TEST_DB_NAME
    TEST_DB_URL=postgresql+asyncpg://${TEST_DB_USER}:${TEST_DB_PASS}@${TEST_DB_HOST}:${TEST_DB_PORT}/${TEST_DB_NAME}
	ENDPOINT_URI
	API_KEY
   ```

2. Установите необходимые зависимости из файла requirements.txt
  ```bash
   pip install -r requirements.txt 
   ```

3. Убедитесь, что Docker и Docker Compose установлены и запущены.

---

## Запуск приложения

1. Запустите контейнер с базой данных с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. После запуска контейнера выполните миграции базы данных:
   ```bash
   alembic upgrade head
   ```

3. Для запуска приложения пропишите команду:
   ```bash
   uvicorn app.main:app --reload
   ```

## Проведение тестов

Для проведения тестов необходимо создать базу данных в контейнере. Для этого выполните следующие команды:

   ```bash
   docker-compose exec db psql -U ${DB_USER} -d ${DB_NAME} -c "CREATE DATABASE ${TEST_DB_NAME};"
   ```

После создания базы данных можно запустить тесты с помощью команды:
   ```bash
   pytest
   ```
   
Документация приложения будет доступно по адресу: [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)

---

## Заключение
Tron Microservice  предоставляет API для взаимодействия с блокчейном Tron, позволяя получать актуальную информацию о состоянии кошельков и их ресурсах, а также сохранять историю запростов в базу данных.
