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

class CreateUpdateUserModel(BaseModel):
    userName: str
    userEmail: str
    userPassword:str
 

class ReadDeleteUserModel(BaseModel):
    userEmail: str
    userPassword:str

@app.get("/")
async def read_root():
    return "Api Working Now"




"""Create New User Post"""
@app.post("/createNewUser/")
async def createNewUserGet(createUpdateUserModel:CreateUpdateUserModel):
    try:
        find_user_doc = collection.count_documents({"user_email":createUpdateUserModel.userEmail}, limit = 1)
        if find_user_doc > 0:
            print("Email Already Exists")
            return {"errors": "Email Already Exists try to login"}
        else:
            insert_obj = collection.insert_one(
                {'user_email': createUpdateUserModel.userEmail,"user_name":createUpdateUserModel.userName,"user_password":createUpdateUserModel.userPassword})
            if insert_obj.acknowledged:
                return {"errors": ""}
            else:
                return {"errors": "User not added"}
    except pymongo.errors.PyMongoError as e:
        print(f"Error in createNewUserGet due to mongo = {e}")
        return {"errors": "User not added"}
    # createNewUserGet("ankit@gmail.com","ankit","hellopassword")


@app.post("/readUsername/")
async def readUsername(readDeleteUserModel:ReadDeleteUserModel):
    find_user_doc = collection.count_documents({"user_email":readDeleteUserModel.userEmail}, limit = 1)
    if find_user_doc > 0:
        check_user_password = collection.count_documents({"user_email":readDeleteUserModel.userEmail,"user_password":readDeleteUserModel.userPassword}, limit = 1)
        if check_user_password>0:
            user_data = collection.find_one({"user_email":readDeleteUserModel.userEmail,"user_password":readDeleteUserModel.userPassword},{"_id":0})
            print(user_data)
            print("login success")
            return {"errors": "","userEmail":user_data["user_email"],"userName":user_data["user_name"],"userPassword":user_data["user_password"]}

        else:
            print("Incorrect Password")
            return {"errors": "Incorrect Password"}
    else:
        print("User not Found")
        return {"errors": "User not Found"}   
    # readUsername("ankit@gmail.com","hellopassword")

@app.post("/updateUsername/")
async def updateUser(createUpdateUserModel:CreateUpdateUserModel):
    update_obj = collection.update_one(
        {
            "user_email": createUpdateUserModel.userEmail,
            "user_password": createUpdateUserModel.userPassword
        },
        {
            "$set": {
                "user_name": createUpdateUserModel.userName
            }
        }
    )
    if update_obj.modified_count>0:
        return {"errors": ""}
    else:
        return {"errors": "Username not updated"}
    # updateUser("ankit@gmail.com","ankitchangede","hellopassword")



@app.post("/deleteUser/")
async def deleteUser(readDeleteUserModel:ReadDeleteUserModel):
    try:
        delete_obj = collection.delete_one({"user_email":readDeleteUserModel.userEmail,"user_password":readDeleteUserModel.userPassword})
        #print(delete_obj.deleted_count)
        if delete_obj.deleted_count >0 :
            return {"errors": ""}
        else:
            return {"errors": "Unable to Delete, Username Or Password is Incorrect !"}
    except pymongo.errors.PyMongoError as e:
        print(f"Error in deleteUser due to mongo = {e}")
        return {"errors": "User not added"}
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
        
createCollection("my_new_collection")
