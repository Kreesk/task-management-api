# Task Management API

Простое приложение для управления задачами с веб-интерфейсом и REST API, построенное на Flask. Позволяет добавлять, редактировать, удалять и отмечать задачи как выполненные через удобный UI или API.

## Особенности
- **Веб-интерфейс**: Управление задачами через браузер с использованием Bootstrap.
- **REST API**: Программный доступ к задачам через endpoints `/api/tasks`.
- **Авторизация**: Защита веб-интерфейса с помощью логина и пароля.
- **База данных**: SQLite для хранения задач.

## Установка

1. Склонируйте репозиторий:

   git clone https://github.com/Kreesk/task-management-api.git
   
   cd task-management-api

2. Создайте виртуальное окружение и активируйте его:

    python -m venv venv

    venv\Scripts\activate  # Windows

    source venv/bin/activate  # Linux/Mac

3. Установите зависимости:

   pip install -r requirements.txt

4. Создайте файл .env для настройки:

   DATABASE=tasks.db
   
   HOST=127.0.0.1
   
   PORT=5000
   
   DEBUG=True

   USERNAME=admin
   
   PASSWORD=password
   

5. Запустите приложение:

   python app.py

6. Откройте в браузере: 

    http://127.0.0.1:8080/

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
2. Введите логин и пароль (по умолчанию admin/password).
3. Введите название задачи в форму и нажмите "Добавить".
4. Нажмите "Done" для завершения задачи.

Технологии
 - Flask
 - Flask-RESTful
 - SQLite
 - Bootstrap 5
 - Python 3

## Скриншоты

   ![image](https://github.com/user-attachments/assets/cbb80a03-14d6-4407-9281-97b5688fdc93)

   ![image](https://github.com/user-attachments/assets/d09b58ac-0515-4a05-a868-697376d6075c)
   
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
