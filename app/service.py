import json
from typing import List, Dict
from pydantic import ValidationError
from app.utils import UserLastState, UserResponse, APP_DIR_ABS_PATH
from redis_om import Migrator


class UsersService:


    def _get_user_by_username(username: str) -> UserLastState:
        """
        Description: get the last saved state for a user based on the user id
        Params:
            username (str): the user id
        Returns:
            (UserLastState): the user last saved state if found 
        """
        try:
            user = UserLastState.find(UserLastState.username == username).all()
            if user:
                return user[0]
        except Exception as e: 
            print(f"UNFOUND USER ID : {username} ", e)
            return None



    @classmethod
    def get_user_last_state_enriched(self, user_name: str) -> UserResponse:
        """
        Description: fetch the last state for the provided username with the organisation tier information
        Args:
            user_name (str): the username
        Return:
            (UserRespone): the user last state with organisation informations
        """
        user_last_state = self._get_user_by_username(user_name)
        
        if not user_last_state:
            return None
            
        user_last_state_enriched = UserResponse(
            username          = user_last_state.username,
            user_type         = user_last_state.user_type,
            organization_name = user_last_state.organization_name,
            organization_tier = user_last_state.organization_tier
        )
        return user_last_state_enriched

    


if __name__ == "__main__":
    print(UsersService.get_user_last_state_enriched("Snake"))
    print(UsersService.get_user_last_state_enriched("M"))
    print(UsersService.get_user_last_state_enriched("Snake"))
    print(UsersService.get_user_last_state_enriched("Snake"))