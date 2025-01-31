from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from . import models, schemas, security
from fastapi import HTTPException, status
from typing import Optional

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[models.User]:
        result = await self.db.execute(
            select(models.User).where(models.User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        result = await self.db.execute(
            select(models.User).where(models.User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        # Check if user already exists
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = security.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password,
            api_key=security.generate_api_key(),
            preferences={}
        )
        
        self.db.add(db_user)
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating user"
            )

    async def authenticate_user(self, email: str, password: str) -> Optional[models.User]:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(self, user_id: int, user_update: schemas.UserUpdate) -> models.User:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user fields
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.preferences is not None:
            db_user.preferences = user_update.preferences

        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error updating user"
            )

    async def regenerate_api_key(self, user_id: int) -> models.User:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.api_key = security.generate_api_key()
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not security.verify_password(current_password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        db_user.hashed_password = security.get_password_hash(new_password)
        await self.db.commit()
        return True