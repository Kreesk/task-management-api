# Task Management API

Простое приложение для управления задачами с веб-интерфейсом и REST API, построенное на Flask. Позволяет добавлять, редактировать, удалять и отмечать задачи как выполненные через удобный UI или API.

## Особенности
- **Веб-интерфейс**: Управление задачами через браузер с использованием Bootstrap.
- **REST API**: Программный доступ к задачам через endpoints `/api/tasks`.
- **Авторизация**: Защита веб-интерфейса с помощью логина и пароля.
- **База данных**: SQLite для хранения задач.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Kreesk/task-management-api.git
   cd task-management-api
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл .env для настройки:
   ```text
   DATABASE=tasks.db
   HOST=0.0.0.0
   PORT=8080
   DEBUG=True
   USERNAME=admin
   PASSWORD=password
   ```
5. Запустите приложение:
   ```bash
   python main.py
   ```
6. Откройте в браузере: 
   ```bash
   http://127.0.0.1:8080/
   ```

## Использование
### Веб-интерфейс
1. Перейдите на http://127.0.0.1:8080/ и нажмите "Начать работу".
2. Введите логин и пароль (по умолчанию admin/password) на /login.
3. Управляйте задачами на http://127.0.0.1:8080/tasks:
   
   - Введите название задачи и нажмите "Добавить".
   - Нажмите "Выполнить" для завершения задачи.
   - Используйте "Редактировать" или "Удалить" для изменения задач.
### REST API

   - Подробности в http://127.0.0.1:8080/api/docs.

#### Примеры API-запросов

   - Получить список всех задач:
     
     ```bash
     curl http://127.0.0.1:8080/api/tasks
     ```
   - Получить одну задачу:
     
     ```bash
     curl http://127.0.0.1:8080/api/tasks/1
     ```
   - Добавить новую задачу:
     
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"title":"Новая задача"}' http://127.0.0.1:8080/api/tasks
     ```
   - Обновить статус задачи:
     
     ```bash
     curl -X PUT -H "Content-Type: application/json" -d '{"status":"done"}' http://127.0.0.1:8080/api/tasks/1
     ```
   - Удалить задачу:
     
     ```bash
     curl -X DELETE http://127.0.0.1:8080/api/tasks/1
     ```
     
## Скриншоты

   ![image](https://github.com/user-attachments/assets/cbb80a03-14d6-4407-9281-97b5688fdc93)

   ![image](https://github.com/user-attachments/assets/d09b58ac-0515-4a05-a868-697376d6075c)

## Технологии
 - Flask
 - Flask-RESTful
 - SQLite
 - Bootstrap 5
 - Python 3

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
