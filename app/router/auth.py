from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import schemas, utils
from app.config import settings
from app.database import User
from app.oauth2 import AuthJWT
from app.serializers.userSerializers import userEntity, userResponseEntity


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
async def create_user(payload: schemas.CreateUserSchema):
    user = User.find_one({"email": payload.email.lower()})
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = "user"
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = userResponseEntity(User.find_one({"_id": result.inserted_id}))

    return {"status": "success", "user": new_user}


@router.post("/login")
def login(
    payload: schemas.LoginUserSchema, response: Response, authorize: AuthJWT = Depends()
):
    db_user = User.find_one({"email": payload.email.lower()})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    user = userEntity(db_user)
    if not utils.verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    access_token = authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )
    refresh_token = authorize.create_refresh_token(
        subject=str(user["id"]),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
    )

    response.set_cookie(
        "access_token",
        access_token,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )

    return {"status": "success", "access_token": access_token}
