**Electives(MakeChoice) MVP** — сервис для управления элективными курсами и выборами студентов.

## Требования

* **Docker** ≥ 28.1.1
* **Docker Compose** ≥ 2.36.0

## Настройка окружения

1. Скопировать файл примера переменных окружения:

   ```bash
   cp example.env .env
   ```
2. Открыть `.env` и указать реальные значения:

   * `DATABASE_URL` (например, `postgresql://postgres:postgres@db:5432/elecdb`)

## Быстрый старт (Docker)

1. Собрать образы:

   ```bash
   make build
   ```
2. Запустить сервисы в фоне:
   ```bash
   make up
   ```
3. Применить миграции:
   ```bash
   make migrate
   ```
4. Открыть в браузере:

   * API:  [http://localhost:8000](http://localhost:8000)
   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)


## 📂 Структура проекта

```
SvetaMakeChoice/
├── migrations/         # Схемы и данные для Alembic
├── src/                # Исходники
│   ├── api/            # HTTP-слой (FastAPI): роутеры, модели, обработка ошибок
│   ├── domain/         # Доменная модель: сущности, интерфейсы репозиториев, UoW, исключения
│   ├── infrastructure/ # Реализация репозиториев (SQLAlchemy), SSO-клиент
│   └── services/       # Бизнес-логика (use cases)
├── test_data/          # Пример CSV для импорта курсов
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md          
```

## Документация API

После старта доступна автоматическая документация:

* **Swagger UI**:  `http://localhost:8000/docs`
