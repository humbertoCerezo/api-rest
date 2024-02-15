from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

#Creación de la APP
app = FastAPI()

#Modelo de usuario
class User(BaseModel):
    id: int
    name: str
    email: str

#Diccionario para guardar datos
users = []

#Expresión regular para el Email
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

@app.get("/")
def index():
    return {"message": "Hola, este es el índice"}

@app.get("/all-users")
def all_users():
    return users

@app.get("/user-detail/{user_id}")
def user_detail(user_id: int):
    for user in users:
        if user.id == user_id: 
            return user
    raise HTTPException(status_code=404, detail="User Not Found")

@app.post("/create-users")
def create_user(user: User):
    if not email_regex.match(user.email):
        raise HTTPException(status_code =401, detail=f"The following email:  '{user.email}' is not valid")
    else:
        users.append(user)
        return {"message": "User created succesfuly"}
    
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "User succesfuly deleted"}
    raise HTTPException(status_code=404, detail="User Not Found")

@app.put("/update-user/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            if not email_regex.match(updated_user.email):
                raise HTTPException(status_code =401, detail=f"The following email:  '{user.email}' is not valid")
            else:
                users[index].name = updated_user.name
                users[index].email = updated_user.email
                return {"message": "User succesfuly updated"}
    raise HTTPException(status_code=404, detail="User Not Found")
"""
Puntos a calificar - API REST:

1.- endpoints:
	- all users [GET] 200, 405(Tras utilizar un método HTTP diferente al correspondiente)
	- user detail [GET] 200, 404(En caso de que no se encuentre la información)
	- create user [POST] 201
	- delete user [DELETE] 200, 404(En caso de que no se encuentre la información)
	- update user [PUT,UPDATE] 200, 404(En caso de que no se encuentre la información)

2.- Modelo de user
	USER:
	- id: int [PK]
	- name: str
	- email: str
3.- Validaciones
	- all fields required [bad request]400
	- email format field [REGEX - expresiones regulares] 400, 422

4.- HTTP Status
	- 200: códigos de estatus satisfactorios
	- 400: Errores de parte del cliente
	- 500: Errores de parte del servidor
"""