from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.core import User, UserSite
from ..core.security import verify_password
from ..core.auth import create_access_token
from ..schemas.auth import LoginRequest, Token, UserResponse
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Get user's assigned sites
    user_sites = db.query(UserSite).filter(UserSite.user_id == user.id).all()
    site_ids = [us.entity_id for us in user_sites]
    
    access_token = create_access_token(subject=user.id, role=user.role, sites=site_ids)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "sites": site_ids
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_sites = db.query(UserSite).filter(UserSite.user_id == current_user.id).all()
    site_ids = [us.entity_id for us in user_sites]
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "sites": site_ids
    }
