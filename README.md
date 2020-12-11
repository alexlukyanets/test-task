## features
- [x] django-taggit
- [x] django-mptt
- [x] Token session
- [x] Tags CRUD API
- [x] User admin panel CRUD
- [x] Admin panel User filter tags
- [x] User custom, custom admin

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
- [x] Docker container.
- [x] Deploy API for testing to Heroku [Heroku app](https://sleepy-beach-16058.herokuapp.com/)
- [x] [Documented with Postman](https://documenter.getpostman.com/view/9950425/TVmV6uJ6#b7e14f8e-98bd-4332-b0ab-3253c82d7ed1)









