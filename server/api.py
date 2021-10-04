from fastapi import FastAPI
import certifi
import pymongo
from fastapi.middleware.cors import CORSMiddleware
from config import *
from pydantic import BaseModel

app = FastAPI()
ca = certifi.where()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_headers=["*"],
    allow_methods=["*"]
)



#db client
client = pymongo.MongoClient(
    db_string, tlsCAFile=ca, connect=False)


#db object
db = client[dbname]

#db access single collection
collection = db["user_list"]

class UserModel(BaseModel):
    userName: str
    userEmail: str
    userPassword:str
 

@app.get("/")
async def read_root():
    return "Api Working"

"""Create New User Get"""
@app.get("/createNewUser/")
async def createNewUserGet(userEmail: str = "",userName:str="",userPassword:str=""):
    try:
        find_user_doc = collection.count_documents({"user_email":userEmail}, limit = 1)
        if find_user_doc > 0:
            print("Email Already Exists")
            return {"errors": "Email Already Exists try to login"}
        else:
            insert_obj = collection.insert_one(
                {'user_email': userEmail,"user_name":userName,"user_password":userPassword})
            if insert_obj.acknowledged:
                return {"errors": ""}
            else:
                return {"errors": "User not added"}
    except pymongo.errors.PyMongoError as e:
        print(f"Error in createNewUserGet due to mongo = {e}")
        return {"errors": "User not added"}
    # createNewUserGet("ankit@gmail.com","ankit","hellopassword")


"""Create New User Post"""
@app.post("/createNewUserPost/")
async def createNewUserGet(userModel:UserModel):
    try:
        find_user_doc = collection.count_documents({"user_email":userModel.userEmail}, limit = 1)
        if find_user_doc > 0:
            print("Email Already Exists")
            return {"errors": "Email Already Exists try to login"}
        else:
            insert_obj = collection.insert_one(
                {'user_email': userModel.userEmail,"user_name":userModel.userName,"user_password":userModel.userPassword})
            if insert_obj.acknowledged:
                return {"errors": ""}
            else:
                return {"errors": "User not added"}
    except pymongo.errors.PyMongoError as e:
        print(f"Error in createNewUserGet due to mongo = {e}")
        return {"errors": "User not added"}
    # createNewUserGet("ankit@gmail.com","ankit","hellopassword")


@app.get("/readUsername/")
async def readUsername(userEmail: str = "",userPassword:str=""):
    find_user_doc = collection.count_documents({"user_email":userEmail}, limit = 1)
    if find_user_doc > 0:
        check_user_password = collection.count_documents({"user_email":userEmail,"user_password":userPassword}, limit = 1)
        if check_user_password>0:
            print("login success")
            return {"errors": ""}

        else:
            print("Incorrect Password")
            return {"errors": "Incorrect Password"}
    else:
        print("User not Found")
        return {"errors": "User not Found"}
        
readUsername("ankit@gmail.com","hellopassword")

@app.get("/updateUsername/")
async def updateUser(userEmail: str = "",userName:str="",userPassword:str=""):
    update_obj = collection.update_one(
        {
            "user_email": userEmail,
            "user_password": userPassword
        },
        {
            "$set": {
                "user_name": userName
            }
        }
    )
    if update_obj.modified_count>0:
        return {"errors": ""}
    else:
        return {"errors": "Username not updated"}
    # updateUser("ankit@gmail.com","ankitchangede","hellopassword")



@app.get("/deleteUser/")
async def deleteUser(userEmail: str = "",userPassword:str=""):
    delete_obj = collection.delete_one({"user_email":userEmail,"user_password":userPassword})
    #print(delete_obj.deleted_count)
    if delete_obj.deleted_count >0 :
        return {"errors": ""}
    else:
        return {"errors": "Unable to Delete, Username Or Password is Incorrect !"}

    # deleteUser("ankit@gmail.co","hellopassword")




"""Print All Collection"""
def allCollection():
    allCollections = db.list_collection_names()
    print(allCollections)
    # allCollection()


"""Create Collection"""
def createCollection(col_name):
    try:
        db.create_collection(col_name)
    except pymongo.errors.PyMongoError as e:
        print(f"Error in createCollection = {e}")
    # createCollection("cool_connection")
