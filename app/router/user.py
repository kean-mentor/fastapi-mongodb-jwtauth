from bson import ObjectId
from fastapi import APIRouter, Depends


from app import oauth2, schemas
from app.database import User
from app.serializers.userSerializers import userResponseEntity


router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(User.find_one({"_id": ObjectId(str(user_id))}))

    return {"status": "success", "user": user}
