from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.db.session import commit_or_rollback, get_db
from app.schemas.user import TokenResponse, UserCreate


router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        # 400: the username is already taken, so we stop before creating another row.
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
    )

    db.add(new_user)
    try:
        commit_or_rollback(db)
    except IntegrityError:
        # 400: another request created the same username before this transaction committed.
        raise HTTPException(status_code=400, detail="User already exists")

    db.refresh(new_user)

    return {"msg": "User created"}


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        # 401: the client sent bad credentials, so no token is issued.
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role
    })

    token = create_access_token({"sub": db_user.username})
    return TokenResponse(access_token=token)
