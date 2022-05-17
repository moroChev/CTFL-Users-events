from fastapi import FastAPI, status, HTTPException
from app.utils import UserResponse
from app.service import UsersService



app = FastAPI()


@app.get(
        "/api/users/{username}", 
        status_code=status.HTTP_200_OK, 
        response_model=UserResponse
    )
def get_user_last_state(username: str):
    """
    Get user last state enriched with organisation informations
    Args:
        username (str): user's username
    Returns:
        (UserResponse): user last state with organisation informations
    """
    if not username:
        raise HTTPException(status_code=400, detail="No username provided")

    user_last_sate = UsersService.get_user_last_state_enriched(user_name=username)
    
    if not user_last_sate:
        raise HTTPException(status_code=404, detail="User not found")
    return user_last_sate