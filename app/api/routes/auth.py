from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.user import User
from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.user import UserCreate
from app.schemas.token import Token

router = APIRouter()

@router.post("/signup", response_model=Token, status_code=201)
async def signup(data: UserCreate, session: AsyncSession = Depends(get_session)):
    
    existing = await session.execute(select(User).where(User.email == data.email))
   
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=data.email, hashed_password=get_password_hash(data.password))
    session.add(user)
    await session.commit()
    token = create_access_token(user.email)
    return Token(access_token=token)

@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
   
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return Token(access_token=token)
