from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app import schemas, utils
from app.database import User
from app.serializers.userSerializers import userResponseEntity


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
