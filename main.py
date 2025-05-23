from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from pydantic import BaseModel
from models import User, LoginRequest, hash_password, verify_password

# ✅ Lifespan decorator properly used
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)

# ✅ MongoDB Connection Setup
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://mulwabenard9507:benard9507@cluster0.xad7ngd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    app.mongodb = app.mongodb_client.get_database("signin_login_page")  # ✅ Use valid name

    collections_to_create = ["logins", "users"]  # ✅ Ensure 'users' collection exists
    existing_collections = await app.mongodb.list_collection_names()

    for collection_name in collections_to_create:
        if collection_name not in existing_collections:
            await app.mongodb.create_collection(collection_name)
            print(f"{collection_name} collection created.")
        else:
            print(f"{collection_name} collection already exists.")
    
    print("MongoDB connected.")

# ✅ Clean shutdown
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")

# ✅ Create FastAPI app
app = FastAPI(lifespan=lifespan)

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to my login page authentication"}

# ✅ Register Endpoint
@app.post("/api/v1/register", response_model=dict)
async def register_user(user: User):
    existing_user = await app.mongodb["users"].find_one({"Email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered with this email.")

    user_dict = user.dict(by_alias=True)
    user_dict["Password"] = hash_password(user_dict["Password"])

    result = await app.mongodb["users"].insert_one(user_dict)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# ✅ Login Endpoint
@app.post("/api/v1/login", response_model=dict)
async def login_user(login: LoginRequest):
    user = await app.mongodb["users"].find_one({"Email": login.email})
    if not user or not verify_password(login.password, user["Password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "username": user["Username"]}

# ✅ Optional: View all users (for debug)
@app.get("/api/v1/users")
async def list_users():
    users = await app.mongodb["users"].find().to_list(length=100)
    for user in users:
        user["_id"] = str(user["_id"])
    return {"users": users}
