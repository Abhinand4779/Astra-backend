from fastapi import APIRouter, HTTPException, Request, Body, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.users import Token, UserResponse, UserSchema
from app.auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from datetime import timedelta
from typing import List
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await request.app.mongodb["users"].find_one({"email": email})
    if user is None:
        raise credentials_exception
    user["_id"] = str(user["_id"])
    return user

async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrative privileges",
        )
    return current_user

@router.post("/register", response_description="Register a new user", status_code=status.HTTP_201_CREATED)
async def register(request: Request, user: UserSchema = Body(...)):
    if await request.app.mongodb["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    
    new_user = await request.app.mongodb["users"].insert_one(user_dict)
    created_user = await request.app.mongodb["users"].find_one({"_id": new_user.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    return created_user

@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await request.app.mongodb["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    access_token = create_access_token(
        data={"sub": user["email"], "is_admin": user.get("is_admin", False)}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/all", response_model=List[dict]) # Use dict to allow extra fields
async def list_all_users(request: Request, admin: dict = Depends(get_current_admin_user)):
    users = []
    cursor = request.app.mongodb["users"].find()
    async for user in cursor:
        user_id_str = str(user["_id"])
        user["id"] = user_id_str
        user["_id"] = user_id_str
        
        # Calculate Stats for this user
        order_count = await request.app.mongodb["orders"].count_documents({"user_id": user_id_str})
        
        total_spent = 0
        user_orders = request.app.mongodb["orders"].find({"user_id": user_id_str})
        async for ord in user_orders:
            try:
                # Extracts numbers from strings like "₹1,500"
                amount_str = "".join(filter(str.isdigit, ord.get("total_amount", "0")))
                total_spent += int(amount_str) if amount_str else 0
            except:
                pass
        
        user["orders"] = order_count
        user["spent"] = f"₹{total_spent:,}"
        user["joining"] = user.get("created_at", datetime.utcnow()).strftime("%d %b %Y")
        
        users.append(user)
    return users
