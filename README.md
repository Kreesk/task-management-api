# Task Management API

Простое веб-приложение для управления задачами, построенное на Flask и Flask-RESTful. 
Поддерживает добавление задач и их просмотр через REST API и HTML-интерфейс.

## Возможности
- Добавление новых задач через POST-запросы к `/api/tasks`.
- Просмотр списка задач через GET-запрос к `/api/tasks` или одной задачи через `/api/tasks/<id>`.
- Обновление статуса задачи через PUT-запрос к `/api/tasks/<id>`.
- Удаление задачи через DELETE-запрос к `/api/tasks/<id>`.
- Хранение задач в базе данных SQLite (`tasks.db`).

## Установка
1. Склонируйте репозиторий:
   git clone https://github.com/Kreesk/task-management-api.git
   cd task-management-api

2. Установите зависимости:
    pip install -r requirements.txt

3. Запустите приложение:
    python app.py

Использование API
GET /api/tasks — получить список всех задач:
curl http://127.0.0.1:5000/api/tasks

GET /api/tasks/<id> — получить одну задачу:
curl http://127.0.0.1:5000/api/tasks/1

POST /api/tasks — добавить новую задачу:
curl -X POST -H "Content-Type: application/json" -d '{"title":"Новая задача"}' http://127.0.0.1:5000/api/tasks

PUT /api/tasks/<id> — обновить статус задачи:
curl -X PUT -H "Content-Type: application/json" -d '{"status":"done"}' http://127.0.0.1:5000/api/tasks/1

DELETE /api/tasks/<id> — удалить задачу:
curl -X DELETE http://127.0.0.1:5000/api/tasks/1

# Просмотр задач
Откройте в браузере: http://127.0.0.1:5000/tasks

# Планы на будущее
   - Исправить поддержку кириллицы (в процессе).
   - Улучшить HTML-страницу (добавить кнопки для управления задачами).
   - Добавить авторизацию.









