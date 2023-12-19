from fastapi import APIRouter, Response,  HTTPException,File, UploadFile
from fastapi.responses import FileResponse
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND , HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema
from schema.user_schema import DataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from os import getcwd

user = APIRouter()

admin = APIRouter()



@user.post("api/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(getcwd() + "/" + file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return "success"  

@user.get("api/file/{name_file}")
def get_file(name_file: str):
    return FileResponse(getcwd() + "/" + name_file)
 




#root
@user.get("/")
async def root():
    return {"message": "Hi, I am a FastAPI route"}


#gettUsers

@user.get("/api/users", response_model=List[UserSchema])
async def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

#gettUse for id

@user.get("/api/user/{user_id}", response_model=UserSchema)
async def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result

#Create users

@user.post("/api/user", status_code=HTTP_201_CREATED)
async def create_user(data_user: UserSchema):
    with engine.begin() as conn:
        new_user = data_user.dict()
        new_user["user_password"] = generate_password_hash(data_user.user_password, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
    return Response(status_code=HTTP_201_CREATED)


#Autenticate whit out token

@user.post("/api/users/login")
async def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        result.id
        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_password)
            if check_passw:
                return  "Succes"
                print(check_passw)
        return  'Denegado'
            
        print(result)


        
#Edit User

@user.put("/api/user/{user_id}", response_model=UserSchema)
async def edit_user(user_id: str, updated_user_id: UserSchema):
    with engine.begin() as conn:
        existing_user = conn.execute(users.select().where(users.c.id == user_id)).first()
        if existing_user:
            password_encrypt = generate_password_hash(updated_user_id.user_password, "pbkdf2:sha256:30", 30)  
            updated_data = {
                "name":updated_user_id.name,
                "username":updated_user_id.username,
                "user_password": password_encrypt
                }
            conn.execute(users.update().values(updated_data).where(users.c.id == user_id))
            return updated_data
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")



        

