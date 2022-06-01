from pydantic import BaseModel, ValidationError, validator
from typing import Optional
from redis_om import HashModel, Field
import os


class UserValidationException(Exception):
    """USER DATA VALIDATION"""


class UserLastState(HashModel):
    user_id: str = Field(index=True)
    username: str = Field(index=True)
    user_type: Optional[str]
    organization_key: Optional[str] 
    organization_name: Optional[str] = Field(index=True)
    organization_tier: Optional[str]
    received_at: str 


class UserResponse(BaseModel):
    username: str
    user_type: str
    organization_name: str
    organization_tier: Optional[str]



APP_DIR_ABS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
   pass

