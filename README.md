# Flask RESTful app

### This API is being developed as a part of Udemy REST APIs with Flask and Python course.

[Course Page](https://www.udemy.com/rest-api-flask-and-python)

This API is built using Flask-RESTful and SQLAlchemy.

#### Main features:

- User model and basic authentication with Flask-JWT
- Store and item models with foreign key relationship
- uWSGI configuration for running the app on Heroku or DigitalOcean

#### Available endpoints

- **/register** (for registering new users)
- **/auth** (for existing user authentication)
- **/stores** (get the list of all stores)
- **/store/name** (get, delete, or post store by name)
- **/items** (get the list of all items)
- **/item/name** (get, delete, or post item by name)
