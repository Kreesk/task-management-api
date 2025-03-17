# Task Management API

Простое веб-приложение для управления задачами, построенное на Flask и Flask-RESTful. Поддерживает создание, просмотр, обновление и удаление задач через REST API, а также их отображение через HTML-интерфейс.

## Возможности
- Создание задач через POST-запросы к `/api/tasks` или форму на странице `/tasks`.
- Просмотр списка задач через GET-запросы к `/api/tasks` или страницу `/tasks`.
- Просмотр одной задачи через GET-запрос к `/api/tasks/<id>`.
- Обновление статуса задач через PUT-запросы к `/api/tasks/<id>`.
- Удаление задач через DELETE-запросы к `/api/tasks/<id>`.
- Хранение задач в базе данных SQLite (по умолчанию `tasks.db`).

## Установка

1. Склонируйте репозиторий:

   git clone https://github.com/Kreesk/task-management-api.git
   
   cd task-management-api

2. Установите зависимости:

   pip install -r requirements.txt

3. Создайте файл .env для настройки:

   DATABASE=tasks.db
   
   HOST=127.0.0.1
   
   PORT=5000
   
   DEBUG=True

5. Запустите приложение:

   python app.py

## Использование API

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

## Использование в браузере

1. Откройте в браузере: http://127.0.0.1:5000/tasks

2. Введите название задачи в форму и нажмите "Добавить".

3. Список задач обновится автоматически.

## Планы на будущее

- Добавить авторизацию для защиты API.
- Расширить функционал: фильтрация задач, категории, дедлайны.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
