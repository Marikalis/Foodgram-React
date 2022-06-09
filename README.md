# FOODGRAM
## Foodgram - это проект «Продуктовый помощник»
## Описание:
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Авторы:
- Ilya Rogozin https://github.com/Marikalis
### Технологии:
- Python 3
- Django 2
- DRF
- Docker

# Как запустить проект:
- Установите Docker, инструкция:
https://docs.docker.com/get-docker/

- Установите docker-compose, инструкция:
https://docs.docker.com/compose/install/

- Клонируйте репозиторий:
```
git clone https://github.com/Marikalis/foodgram-project-react.git
```

- Создайте в папках backend/ и infra/ файл окружения .env, который будет содержать:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY = 'pYA-zPk2GJA8WOXiOY67L8eMJ9ikdQXVNj_fNwfW4TE'

SERVER_NAMES = '62.84.120.222 127.0.0.1 localhost'
DEBUG = True
```

- Соберите контейнеры и запустите их из папки foodgram-project-react/infra:
```
docker-compose up -d --build
```

#### Установите подсветку синтаксиса терминала bash:
- Откройте конфигурационный файл:
```
nano /etc/skel/.bashrc
```
- Раскомментите строку __force_color_prompt=yes__
- Примените изменения:
```
source /etc/skel/.bashrc
```
-----------------------------------------------------

#### Далее все команды выполняйте из папки infra/
- Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```

- Создайте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

- Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

- Заполните БД начальными данными:
```
docker-compose exec backend python manage.py loadjson --path 'data/ingredients.json'
docker-compose exec backend python manage.py loadjson --path 'data/tags.json'
```

## Примеры запросов к API можно посмотреть по запросу:
http://62.84.120.222/api/docs/

## Главная страница:
http://62.84.120.222
