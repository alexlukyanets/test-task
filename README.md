
## Коментарий от разработчика
Дорого времени суток. Спасибо, за данное тестовое задание. Выполнять его было интересно. 
Если б было чуть больше времени, можно было доделать слабые места проекта, а именно:
- Доделать Posman документацию
- Кое-где криво написан код
- Полностью тестировать heroku приложение 
- Оптимизировать запросы

## Features
- :heavy_check_mark: django-taggit
- :heavy_check_mark: django-mptt
- :heavy_check_mark: Token session
- :heavy_check_mark: Tags CRUD API
- :heavy_check_mark:  User admin panel CRUD
- :heavy_check_mark: Admin panel User filter tags
- :heavy_check_mark: User custom, custom admin
 
 ## GET /tags/
- list with hierarchy, Access: any users
- CRUD only admins and is_customer_admin = true
- User by tag

## GET /users_list/
- User registered list only is_customer_admin

## GET /user_tag/id
- Get requested user tags without id
- Get tags from other user, use id, only is_customer_admin
- Create Update Tags

## Skills
- :heavy_check_mark: Docker container.
- :heavy_check_mark:  Deploy API for testing to [Heroku app](https://sleepy-beach-16058.herokuapp.com/)
- :heavy_check_mark:  Documented with [Postman](https://documenter.getpostman.com/view/9950425/TVmV6uJ6#de0a46d8-b378-4b16-a285-718e3c738613)
