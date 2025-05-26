from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from models import User, LoginRequest, hash_password, verify_password

# ✅ MongoDB connection lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)

# ✅ MongoDB connection setup
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://mulwabenard9507:benard9507@cluster0.xad7ngd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    app.mongodb = app.mongodb_client.get_database("signin_login_page")

    collections = ["users", "logins"]
    existing = await app.mongodb.list_collection_names()

    for name in collections:
        if name not in existing:
            await app.mongodb.create_collection(name)
            print(f"Created collection: {name}")
        else:
            print(f"Collection '{name}' already exists.")
    print("✅ MongoDB connected.")

# ✅ MongoDB shutdown
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("🔌 Database connection closed.")

# ✅ Create FastAPI app
app = FastAPI(title="Login/Register API", version="1.0", lifespan=lifespan)

# ✅ Health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Login/Register API"}

# ✅ Registration endpoint
@app.post("/register", status_code=201)
async def register_user(user: User):
    existing = await app.mongodb["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already registered with this email.")

    hashed_pw = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_pw
    }

    result = await app.mongodb["users"].insert_one(user_data)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# ✅ Login endpoint
@app.post("/login")
async def login_user(login: LoginRequest):
    user = await app.mongodb["users"].find_one({"email": login.email})
    if not user or not verify_password(login.password, user.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "username": user["username"],
        "email": user["email"]
    }

# ✅ Optional: View all users (debug only!)
@app.get("/users")
async def list_users():
    users = await app.mongodb["users"].find().to_list(length=100)
    for user in users:
        user["_id"] = str(user["_id"])
        user.pop("hashed_password", None)
    return {"users": users}
