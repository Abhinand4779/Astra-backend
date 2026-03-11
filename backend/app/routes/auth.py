from fastapi import APIRouter, HTTPException, Request, Body, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.users import Token, UserResponse, UserSchema
from app.auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from datetime import datetime, timedelta
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

@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, request: Request, admin: dict = Depends(get_current_admin_user)):
    from bson import ObjectId
    try:
        delete_result = await request.app.mongodb["users"].delete_one({"_id": ObjectId(user_id)})
        if delete_result.deleted_count == 1:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID format or server error")

@router.get("/all", response_model=List[dict])
async def list_all_users(request: Request, admin: dict = Depends(get_current_admin_user)):
    try:
        users = []
        cursor = request.app.mongodb["users"].find()
        async for user in cursor:
            # Create a clean dict to avoid returning password hash and handle ObjectId
            user_id_str = str(user.get("_id"))
            
            # Calculate Stats safely
            order_count = await request.app.mongodb["orders"].count_documents({"user_id": user_id_str})
            
            total_spent = 0
            user_orders_cursor = request.app.mongodb["orders"].find({"user_id": user_id_str})
            async for ord_doc in user_orders_cursor:
                try:
                    # Clean currency string e.g., "₹1,500" -> 1500
                    amount_str = "".join(filter(str.isdigit, str(ord_doc.get("total_amount", "0"))))
                    total_spent += int(amount_str) if amount_str else 0
                except:
                    pass
            
            # Safe Date formatting
            joining_date = user.get("created_at")
            if not isinstance(joining_date, datetime):
                joining_date = datetime.utcnow()
                
            users.append({
                "_id": user_id_str,
                "id": user_id_str,
                "name": user.get("name", "Unknown"),
                "email": user.get("email"),
                "is_admin": user.get("is_admin", False),
                "orders": order_count,
                "spent": f"₹{total_spent:,}",
                "joining": joining_date.strftime("%d %b %Y"),
                "status": "Active"
            })
        return users
    except Exception as e:
        print(f"Error in list_all_users: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error fetching customer directory")
