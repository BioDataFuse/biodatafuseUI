from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from . import schemas, security, services
from .database import get_db
from typing import Optional
from jose import JWTError, jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user_service = services.UserService(db)
    user = await user_service.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/register", response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    return await user_service.create_user(user)

@router.post("/auth/login", response_model=schemas.Token)
async def login(
    login_data: schemas.LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    user = await user_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/user", response_model=schemas.UserResponse)
async def get_user_info(current_user = Depends(get_current_user)):
    return current_user

@router.put("/auth/profile", response_model=schemas.UserResponse)
async def update_profile(
    user_update: schemas.UserUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    return await user_service.update_user(current_user.id, user_update)

@router.post("/auth/regenerate-api-key", response_model=schemas.UserResponse)
async def regenerate_api_key(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    return await user_service.regenerate_api_key(current_user.id)

@router.put("/auth/password")
async def change_password(
    password_update: schemas.PasswordUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = services.UserService(db)
    return await user_service.update_password(
        current_user.id, 
        password_update.current_password,
        password_update.new_password
    )

@router.post("/auth/logout")
async def logout():
    # In this simple implementation, we don't need to do anything
    # as the token is managed client-side
    return {"message": "Successfully logged out"}