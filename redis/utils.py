from typing import Optional, Dict
from docker import DockerClient
from pydantic import ValidationError
from redis_om import HashModel, Field


class UserEvent(HashModel):
    user_id: str = Field(index=True)
    event_type: str 
    username: str = Field(index=True)
    user_email: str 
    user_type: str  
    organization_name: str  
    received_at: str 


class OrgEvent(HashModel):
    organization_key: str = Field(index=True)
    organization_name: str
    organization_tier: Optional[str]
    created_at: str


class UserLastState(HashModel):
    user_id: str = Field(index=True)
    username: str
    user_type: Optional[str]
    organization_key: Optional[str] 
    organization_name: Optional[str] = Field(index=True)
    organization_tier: Optional[str]
    received_at: str 


class UserValidationException(Exception):
    """USER DATA VALIDATION"""



def parse_user_event(user_event: Dict[str, str]) -> UserEvent:
    try:
        user_event = UserEvent(**user_event)
        return user_event
    except ValidationError as e:
        print(f"ERROR IN PARSING {e} USER EVENT {user_event} WILL BE IGNORED ")
        return None


def parse_org_event(org_event: Dict[str, str]) -> OrgEvent:
    try:
        org_event = OrgEvent(**org_event)
        return org_event
    except ValidationError as e:
        print(f"ERROR IN PARSING {e} ORG EVENT {org_event} WILL BE IGNORED ")
        return None


def get_container_ip_address(container_name: str, network_name: str) -> str:
    """
    Description: get the container ip address in the provided network
    Params:
        container_name (str) : the container name
        network_name (str) : the container network
    Return:
        (str) : the ip address
    """
    container = DockerClient().containers.get(container_name)
    return container.attrs["NetworkSettings"]["Networks"][network_name]["IPAddress"]



if __name__ == "__main__":
    a_event = {'user_id': 'bd4a5c7eebced7dc9221f089c164fcb7', 'event_type': 'User Created', 'username': '', 'user_email': '', 'user_type': '', 'organization_name': 'Factorio', 'received_at': '2020-12-09 20:03:16.759617'}
    user_event = UserEvent(**a_event)
    last = UserLastState(**user_event.dict())
    print(last)
    
