## Features
- django-taggit
- django-mptt
- Token session
- Tags CRUD API
- User admin panel CRUD
- Admin panel User filter tags
- User custom, custom admin
 
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
- Docker container.
- Deploy API for testing to Heroku Heroku app
- Documented with Postman
