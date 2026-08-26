# TaxiAPI

REST API для сервиса такси, разпработанный спомощью FastAPI  
----------------------------------------------------
## Возможности
- Пользователь:
  - Поиск свободных активных водителей
  - Получение информации о своём профиле
  - Создание поездки на указаный адресс
  - Добавление отзывов и оценок водителю к прошедшим заказам
  - Просмотр своих написанных ранее отзывов
- Водитель:
  - Подтверждение поездки
  - Получение активной поездки
  - Завершение поездки
  - Просморт своих отзывов и оценки
- Администратор:
  - Добавление новых водителей
  - Блокировка водителей
  - Разблокрировка водителей
- Авторизация:
   - Регистрация новых пользователей
   - Верификация пользователя
   - Повторное отправление кода верификации
   - Обновление access token спомощью refresh token
   - Авторизация пользователей  
----------------------------------------------------
### Технологии  
[Язык програмирования - _Python_](https://www.python.org/ "Официальный сайт python с инструкцией по установке, документацией, новыми релизами и сообществом")  
<img alt="Python" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1280px-Python-logo-notext.svg.png?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail" width="30" height="30"/>  
[Система управления базой данных - _PostgreSQL_](https://www.postgresql.org/ "Официальный сайт postgresql с инструкцией по установке, документацией и сообществом")  
<img alt="PostgreSQL" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/250px-Postgresql_elephant.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail" width="30" height="30"/>  
[SQLAlchemy](https://www.sqlalchemy.org/)  
<img alt="SQLAlchemy" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjigSp6PYwwdfWb42MsT5LmWy4kyfBJYZCVXZNlenpCA&s=10" width="60" height="30"/>  
[JSON Web Tokens](https://www.jwt.io/)  
<img alt="JWT" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2DRF3Tz-_FhNH9B2bYdAAwvrYo_EZ-k1wo5Oc4zR_5W5NEy-Few8ixmk&s=10" width="60" height="30"/>  
[Pydantic](https://avatars.githubusercontent.com/u/110818415?s=200&v=4)  
<img alt="Pydantic" src="https://avatars.githubusercontent.com/u/110818415?s=200&v=4" width="30" height="30"/>

Другие библиотеки и технологии:  
- _aiosmtplib_
- _brypt_
- _hashlib_
- _password\_validator_
- _email\_valdiator_  

-----------------------------------
### Структура проекта

```text
TaxiAPI/
|--- api/
|--- auth/
|--- core/
|--- models/
|--- repositories/
|--- routers/
|--- schemas/
|--- service/
```

/api - основной запуск проекта  
/auth - утилиты дял выпуска и верификации токенов и паролей. Зависимости FastAPI  
/core - подключение к СУБД и `enum.Enum` классы  
/models - orm модели  
/repositories - ООП общения с базой данных  
/routers - endpoints для RestAPI  
/schemas - pydantic схемы  
/service - бизнес логика проекта  
----------------------------
###  Пример TaxiAPI\core\.env файла
```python
DB_USER=username
DB_PASSWORD=password
DB_HOST=database host
DB_PORT=database port
DB_NAME=database name
SANDBOX_USERNAME=username
SANDBOX_PASSWORD=password
```
Переменнные DB_USER, DB_PASSWORD, DB_HOST, DB_PORT используються для установки подключения к СУБД в `core\setting.py`  
```py
url = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"
```
Переменные SANDBOX_USERNAME, SANDBOX_PASSWORD используються для имитации отправки електронных писем на платформе [mailtrap](https://mailtrap.io/) в `service\send_email.py`  
```python
    result = await aiosmtplib.send(
        message,
        hostname="sandbox.smtp.mailtrap.io",
        port=2525,
        username=os.getenv("SANDBOX_USERNAME"),
        password=os.getenv("SANDBOX_PASSWORD"),
        start_tls=True,
    )
```
