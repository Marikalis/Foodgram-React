# FOODGRAM
## Foodgram - The “Grocery Assistant” Project
## Description:
This service allows users to publish recipes, follow other users' publications, add save recipes to a "Favorites" list, and download a consolidated list of ingredients needed to prepare one or more selected dishes before going shopping.
### Authors:
- Maria Lisitskaya https://github.com/Marikalis
### Technologies:
- Python 3
- Django 2
- DRF
- Docker

# How to start the project:
- Install Docker, instructions:
https://docs.docker.com/get-docker/

- Install docker-compose, instructions:
https://docs.docker.com/compose/install/

- Clone the repository:
```
git clone https://github.com/Marikalis/foodgram-project-react.git
```

- Create an environment file `.env` in the backend/ and infra/ folders that will contain:
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

- Build and run the containers from the foodgram-project-react/infra folder:
```
docker-compose up -d --build
```

#### Set up bash terminal syntax highlighting:
- Open the configuration file:
```
nano /etc/skel/.bashrc
```
- Uncomment the line __force_color_prompt=yes__
- Apply the changes:
```
source /etc/skel/.bashrc
```
-----------------------------------------------------

#### Execute the following commands from the infra/ folder:
- Perform migrations:
```
docker-compose exec backend python manage.py migrate
```

- Create a superuser:
```
docker-compose exec backend python manage.py createsuperuser
```

- Collect static files:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

- Populate the DB with initial data:
```
docker-compose exec backend python manage.py loadjson --path 'data/ingredients.json'
docker-compose exec backend python manage.py loadjson --path 'data/tags.json'
```

## Examples of API requests can be seen at:
http://62.84.120.222/api/docs/

## Homepage:
http://62.84.120.222

================================================================

# FOODGRAM
## Foodgram - это проект «Продуктовый помощник»
## Описание:
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Авторы:
- Maria Lisitskaya https://github.com/Marikalis
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
