from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.schemas.user import UserLogin
from fastapi.security import OAuth2PasswordRequestForm

class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user: UserCreate,
    ):
        # Step 1: Check if email already exists
        stmt = select(User).where(User.email == user.email)

        result = db.execute(stmt)

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Step 2: Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role,
        )

        # Step 3: Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login(
            db: Session,
            form_data: OAuth2PasswordRequestForm,
    ):
        stmt = select(User).where(
            User.email == form_data.username
        )

        result = db.execute(stmt)

        existing_user = result.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        if not verify_password(
                form_data.password,
                existing_user.hashed_password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": existing_user.email,
                "role": existing_user.role.value,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }