# Foodgram
![Foodgram workflow](https://github.com/tomatoinoil/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Оглавление
1. [Описание проекта](https://github.com/TomatoInOil/foodgram-project-react#описание-проекта)
2. [Как развернуть?](https://github.com/TomatoInOil/foodgram-project-react#как-развернуть)
3. [Примеры запросов и ответов](https://github.com/TomatoInOil/foodgram-project-react#примеры-запросов-и-ответов) 
4. [Об авторe](https://github.com/TomatoInOil/foodgram-project-react#об-авторe)
## Описание проекта
Приложение **«Продуктовый помощник»**: сайт, на котором пользователи могут *публиковать рецепты*, *добавлять чужие рецепты в избранное* и *подписываться на публикации других авторов*. Сервис **«Список покупок»** позволяет пользователям перед походом в магазин *скачивать сводный список продуктов*, необходимых для приготовления одного или нескольких выбранных блюд.
## Как развернуть?
- Склонировать репозиторий.
```BASH
git clone https://github.com/TomatoInOil/foodgram-project-react.git
```
- Установить `Docker`. Инструкция по установке есть в [официальной документации](https://docs.docker.com/engine/install/ubuntu/).
- Установить `docker-compose`. Инструкция по установке есть в [официальной документации](https://docs.docker.com/compose/install/linux/).
- Перейти в директорию `infra`.
```BASH
cd infra/
```
- Создать и заполнить `.env` нужными переменными окружения. Шаблон заполнения можно найти в этой же директории под именем `example.env`.
- В проекте используется протокол HTTPS, поэтому `nginx` не запуститься если криптографические сертификаты отсутствуют. Чтобы всё заработало, нужно создать фиктивные сертификаты, запустить nginx, удалить фиктивные и запросить реальные сертификаты. Я использовал для этого скрипт, написанный [Philipp](https://github.com/wmnnd/nginx-certbot). Итак, скачивается он следующей командой.
```BASH
curl -L https://raw.githubusercontent.com/wmnnd/nginx-certbot/master/init-letsencrypt.sh > init-letsencrypt.sh
```
- Отредактируем скрипт, заменив `data_path="./data/certbot"` на `data_path="./certbot"`, добавив свой *email* и заменив `example.org www.example.org` в `domains=(example.org www.example.org)` на домен по которому будет доступен наш проект. Далее запустим его.
```BASH
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```
- Запустить `docker-compose`.
```BASH
docker-compose up -d
```
- Можно добавить более 2000 ингредиентов *management*-командой `loadingredients`.
```BASH
docker-compose exec backend python manage.py loadingredients
```
- Создать суперпользователя.
```BASH
docker-compose exec backend python manage.py createsuperuser
```
## Примеры запросов и ответов
Основной функционал
- Найти рецепты на главной странице: `https://.../recipes`  
- Заходить на страницы других пользователей: `https://.../user/{{ id }}`  
- Переходить на страницы рецептов с их описанием: `https://.../recipes/{{ id }}`  
- Подписываться на авторов и просматривать их рецепты на странице «Мои подписки»: `https://.../subscriptions`  
- Добавлять рецепты в избранное и просматривать их на странице «Избранное»: `https://.../favorites`  
- Добавлять рецепты в избранное, чтобы потом скачать список нужных ингрединетов на странице «Список покупок»: `https://.../cart`  
- Опубликовывать свои рецепты с помощью формы на странице «Создать рецепт»: `https://.../recipes/create`  
- Изменять свой пароль: `https://.../change-password`  
- И выходить из системы, нажатием на кнопку `выход` в верхнем углу интерфейса.  
  
После того, как проект [развёрнут](https://github.com/TomatoInOil/foodgram-project-react#как-развернуть), документацию по API можно найти на эндпоинте `https://.../api/docs/`.
## Об авторe
Над проектом работал [Даниил Паутов](https://github.com/TomatoInOil), студент Яндекс.Практикума.
