from pydantic import BaseModel, ValidationError, validator
from typing import Optional
import os


class UserValidationException(Exception):
    """USER DATA VALIDATION"""


class UserEvent(BaseModel):
    id: str 
    event_type: str 
    username: str 
    user_email: Optional[str] 
    user_type: str 
    organization_name: str 
    received_at: str 


class OrgEvent(BaseModel):
    organization_key: str
    organization_name: str
    organization_tier: Optional[str]
    created_at: str


class UserResponse(BaseModel):
    username: str
    user_type: str
    organization_name: str
    organization_tier: Optional[str]



APP_DIR_ABS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
    a = UserEvent(
        id="", 
        event_type="EVENT TYPE str", 
        username="USER NAME", 
        user_email="USER EMAIL str", 
        user_type="USER TYPE str", 
        organization_name="ORG NAME str", 
        received_at="RECEIVED AT str"
    )
    print(a.id)

