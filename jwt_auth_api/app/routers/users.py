
from fastapi import APIRouter, Depends
from jwt_auth_api.app.dependencies import get_current_user
from jwt_auth_api.app.models import User
from jwt_auth_api.app.schemas import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/protected")
def protected_data(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "You have accessed protected data!",
        "user_id": current_user.id,
        "email": current_user.email
    }
