"""
OcchioEsperto.it — Authentication router.
Registration, login, profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..database import get_db, User, UserRole, UserPlan
from ..auth import (
    hash_password, verify_password, create_access_token,
    get_current_user,
)
from ..config import DISCLAIMER, AUTH_RATE_LIMIT
from ..utils import sanitize_string
from ..services.email_service import send_welcome_email

router = APIRouter(prefix="/api", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


# --- Pydantic schemas ---

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)  # min 8 chars now
    name: str = Field(default="", max_length=255)
    plan: str = Field(default="free", description="Piano: free, intermedio, avanzato")


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
@limiter.limit(AUTH_RATE_LIMIT)
def register(request: Request, req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account."""
    # Sanitize inputs
    email = req.email.strip().lower()
    name = sanitize_string(req.name, max_length=255)

    # Check if email already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email già registrata",
        )

    # Password strength validation
    password = req.password
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La password deve essere di almeno 8 caratteri",
        )

    # Create user with sanitized data
    user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
        role=UserRole.USER,
        plan=UserPlan.FREE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token(data={"sub": str(user.id), "email": user.email})

    # Send welcome email (async, non bloccante)
    send_welcome_email(user.email, user.name)

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
@limiter.limit(AUTH_RATE_LIMIT)
def login(request: Request, req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and receive JWT token."""
    # Sanitize email
    email = req.email.strip().lower()

    user = db.query(User).filter(User.email == email).first()
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
    # Sanitize name
    clean_name = sanitize_string(name, max_length=255)
    if clean_name:
        current_user.name = clean_name
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