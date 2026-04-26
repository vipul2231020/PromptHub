from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logger import get_logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = get_logger(__name__)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.....Bhai aap toh purane chawal ho",
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"New user registered: {user.email}")
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT token."""
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password....What brother password bhool jate ho toh google password me save kr liya kro",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive....Bhai aapka toh dead hai....Account",
        )

    token = create_access_token(data={"sub": str(user.id)})
    logger.info(f"User logged in: {user.email}")

    return TokenResponse(access_token=token)
