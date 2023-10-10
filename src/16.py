from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
db = []


class User(BaseModel):
    """A class representing user data with the following attributes"""
    id: int
    firstname: str
    lastname: str
    age: int


@app.get('/')
def read_user() -> str:
    """The function returns a welcome message"""
    return f'Hello'


@app.get('/retrieve')
def retrieve(user_id: int) -> str | dict:
    """A function to retrieve data by id"""
    for index, data in enumerate(db):
        if data['id'] == user_id:
            return db[index]
    return 'not exist'


@app.post('/create_user')
def create_user(user: User) -> dict:
    """The function allows to create a new user by data"""
    new_user = user.dict()
    db.append(new_user)
    return new_user


@app.put('/create_update_user')
def create_update_user(user: User) -> dict:
    """The function allows to either create a new user or update an existing user's data"""
    user_data = user.dict()
    for index, data in enumerate(db):
        if data['id'] == user_data['id']:
            db[index] = user_data
            return user_data
    db.append(user_data)
    return user_data


@app.patch('/update_user')
def update_user(user: User) -> dict:
    """The function allows update an existing user's data"""
    user_data = user.dict()
    for index, data in enumerate(db):
        if data['id'] == user_data['id']:
            if 'firstname' in user_data:
                data['firstname'] = user_data['firstname']
            if 'lastname' in user_data:
                data['lastname'] = user_data['lastname']
            if 'age' in user_data:
                data['age'] = user_data['age']
            return user_data


@app.delete('/delete_user')
def delete_user(user: User) -> str:
    """The function allows you to delete a user from the database based on id"""
    user_data = user.dict()
    for index, data in enumerate(db):
        if data['id'] == user_data['id']:
            db.pop(index)
            return 'deleted'
    return 'not exist'


@app.head('/head')
def head(url: str) -> dict:
    """The function allows to send a HEAD request to a specified URL and retrieve the response headers"""
    return requests.head(url)


@app.options('/options')
def options(url: str) -> str:
    """The function allows to send an OPTIONS request to a specified URL and retrieve information about the response"""
    response = requests.options(url)
    return f""" Status code = {response.status_code}, 
                Headers = {response.headers}, 
                Allow = {response.headers.get('Allow')}"""
