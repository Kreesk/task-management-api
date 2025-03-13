# Task Management API

Простое веб-приложение для управления задачами, построенное на Flask и Flask-RESTful. Поддерживает добавление задач и их просмотр через REST API и HTML-интерфейс.

## Возможности
- Добавление новых задач через POST-запросы к `/api/tasks`.
- Просмотр списка задач через GET-запросы к `/api/tasks` или HTML-страницу `/tasks`.
- Асинхронный запуск с использованием `uvicorn`.

## Установка
1. Склонируйте репозиторий:
   git clone https://github.com/Kreesk/task-management-api.git
   cd task-manager

2. Установите зависимости:
    pip install -r requirements.txt

3. Запустите приложение:
    python app.py

# Использование API

GET /api/tasks — получить список всех задач.
    curl http://127.0.0.1:5000/api/tasks

POST /api/tasks — добавить новую задачу.
    curl -X POST -H "Content-Type: application/json" -d '{"title":"Новая задача"}' http://127.0.0.1:5000/api/tasks

# Просмотр задач
Откройте в браузере: http://127.0.0.1:5000/tasks

# Планы на будущее
## Добавить базу данных SQLite для постоянного хранения задач.

## Реализовать обновление и удаление задач.

## Добавить авторизацию.









