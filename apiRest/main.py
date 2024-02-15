from fastapi import FastAPI, HTTPException
#Librería que importa una "validación" para los modelos
from pydantic import BaseModel
#Librería que importa función para que sea opcional un tipo de dato
from typing import Optional
#Librería para expresiones regulares
import re
#Librería para generación de id's únicos
from uuid import uuid4


#Se crea la aplicación llamada "app"
app = FastAPI()

#Expresión regular para el Email
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

#Diccionario que simule la creación de usuarios
users = []

#Aquí se genera un modelo para cuando se use el método POST
class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    #Para que sea opcional un tipo de dato se agrega Optional[tipoDeDato]
    editorial: Optional[str]


class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/")
def index():
    return {"message": "Hola"}


@app.get("/all-users")
def show_users(user: User):
    return {User}

# Creación de usuario 
@app.post("/create-user")
def create_user(user: User):
    if not email_regex.match(user.email):
        raise HTTPException(status_code =401, detail=f"Email {user.email} not valid")
    else:
        users.append(user)
        return users
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