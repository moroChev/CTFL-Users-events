from pydantic import BaseModel, ValidationError, validator
from typing import Optional, List, Dict
from docker import DockerClient
import json
import os


class UserValidationException(Exception):
    """USER DATA VALIDATION"""


class UserEvent(BaseModel):
    user_id: str 
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


APP_DIR_ABS_PATH = os.path.abspath(os.path.dirname(__file__))
USER_EVENTS_FILE = f"{APP_DIR_ABS_PATH}/data/user_events.json"
ORG_EVENTS_FILE  = f"{APP_DIR_ABS_PATH}/data/org_events.json"


def read_user_events_file() -> List[Dict[str, str]]:
    """
    Description: Read user events file
    Return: 
        (List[Dict[str, str]]): list of user events dictionaries
    """
    with open(USER_EVENTS_FILE) as f:
        return json.load(f)


def read_org_events_file() -> List[Dict[str, str]]:
    """
    Description: Read organisation events file
    Return: 
        (List[Dict[str, str]]): list of organisation events dictionaries
    """
    with open(ORG_EVENTS_FILE) as f:
        return json.load(f)


def get_user_events_parsed() -> List[UserEvent]:
    """
    Description: Parse user events from file to UserEvent Objects, and ignore malformed events
    Return:
        (List[UserEvent]) : list of well formed user events objects
    """
    user_events = read_user_events_file()
    user_events_objects = []
    for user_event in user_events:
        try:
            user_event = UserEvent(**user_event)
            user_events_objects.append(user_event)
        except ValidationError as e:
            continue
            #print("MALFORMED USER EVENT IGNORED : ", user_event)
    return user_events_objects


def get_org_events_parsed() -> List[OrgEvent]:
    """
    Description: Parse organisation events from file to orgEvent Objects, and ignore malformed events
    Return:
        (List[orgEvent]) : list of well formed org events objects
    """
    org_events = read_org_events_file()
    org_events_objects = []
    for org_event in org_events:
        try:
            org_event = OrgEvent(**org_event)
            org_events_objects.append(org_event)
        except ValidationError as e:
            continue
            #print("MALFORMED org EVENT IGNORED : ", org_event)
    return org_events_objects


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
    print(get_container_ip_address("api", "apps-network"))
    containers = DockerClient().containers.list(all=True)
    for con in containers:
        if con.name == "kafka":
            #print(con.attrs)
            continue
    

