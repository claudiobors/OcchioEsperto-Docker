"""
OcchioEsperto.it — Authentication router.
Registration, login, profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from ..database import get_db, User, UserRole, UserPlan
from ..auth import (
    hash_password, verify_password, create_access_token,
    get_current_user,
)
from ..config import DISCLAIMER

router = APIRouter(prefix="/api", tags=["auth"])


# --- Pydantic schemas ---

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    name: str = Field(default="", max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
    disclaimer: str = DISCLAIMER


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    plan: str
    is_active: bool
    disclaimer: str = DISCLAIMER

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
    disclaimer: str = DISCLAIMER


# --- Endpoints ---

@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account."""
    # Check if email already exists
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email già registrata",
        )

    # Create user
    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        name=req.name,
        role=UserRole.USER,
        plan=UserPlan.FREE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
            "plan": user.plan.value,
        },
    )


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and receive JWT token."""
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password non validi",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account disattivato",
        )

    token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return TokenResponse(
        access_token=token,
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
            "plan": user.plan.value,
        },
    )


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role.value,
        plan=current_user.plan.value,
        is_active=current_user.is_active,
    )


@router.put("/me", response_model=UserResponse)
def update_profile(
    name: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile."""
    if name:
        current_user.name = name
    db.commit()
    db.refresh(current_user)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role.value,
        plan=current_user.plan.value,
        is_active=current_user.is_active,
    )