## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/hrapovd1/api_final_yatube.git
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

для версий python >= 3.8 стоит выполнить команду:
```
pip3 install wheel
```

после чего:

```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Создать пользователя:

```
python3 manage.py shell
>>> from posts.models import User
>>> user = User.objects.create(username='user')
>>> user.set_password('secured_password')
>>> user.save()
```

## Примеры запросов API

### Получить JWT токен

запрос:
```
curl --location --request POST '127.0.0.1:8000/api/v1/jwt/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "user",
    "password": "secured_password"
}'
```

ответ:
```
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDEzODg1MSwianRpIjoiMzc4NTRkZjNiMDY5NGVhZWI5NzJjMDBmYWM4YjI3ZjgiLCJ1c2VyX2lkIjoxfQ.ExWViLjkihGTr--IIH32Uv2qZbNcNAjMo5O4_7nBKwI","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMTM4ODUxLCJqdGkiOiI1NjBmMGJmZDFhNjY0YjYxODY1Y2ZmNjFiNjdmOWM5YyIsInVzZXJfaWQiOjF9.vxy1S9izX_SfaRvsGz-8VfGON3gY1I_K56ZybWx4k2w"}
```

### Получить список постов

запрос:
```
curl --location --request GET '127.0.0.1:8000/api/v1/posts/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMTM4ODUxLCJqdGkiOiI1NjBmMGJmZDFhNjY0YjYxODY1Y2ZmNjFiNjdmOWM5YyIsInVzZXJfaWQiOjF9.vxy1S9izX_SfaRvsGz-8VfGON3gY1I_K56ZybWx4k2w' \
--header 'Content-Type: application/json'
```

ответ:
```
[{"id":1,"author":"user","image":null,"group":null,"text":"Test post.","pub_date":"2022-08-09T13:44:35.082205Z"}]
```

### Создать пост

запрос:
```
curl --location --request POST '127.0.0.1:8000/api/v1/posts/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMTM4ODUxLCJqdGkiOiI1NjBmMGJmZDFhNjY0YjYxODY1Y2ZmNjFiNjdmOWM5YyIsInVzZXJfaWQiOjF9.vxy1S9izX_SfaRvsGz-8VfGON3gY1I_K56ZybWx4k2w' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Test post2."
}'
```
ответ:
```
{"id":2,"author":"user","image":null,"group":null,"text":"Test post2.","pub_date":"2022-08-09T13:46:14.411611Z"}
```