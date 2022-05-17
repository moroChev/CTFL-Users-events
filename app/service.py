import json
from typing import List, Dict
from pydantic import ValidationError
from app.utils import UserEvent, OrgEvent, UserResponse, APP_DIR_ABS_PATH



class UsersService:


    USER_EVENTS_FILE = f"{APP_DIR_ABS_PATH}/data/user_events.json"
    ORG_EVENTS_FILE  = f"{APP_DIR_ABS_PATH}/data/org_events.json"

    
    def read_user_events_file(self) -> List[Dict[str, str]]:
        """
        Description: Read user events file
        Return: 
            (List[Dict[str, str]]): list of user events dictionaries
        """
        with open(self.USER_EVENTS_FILE) as f:
            return json.load(f)


    def read_org_events_file(self) -> List[Dict[str, str]]:
        """
        Description: Read organisation events file
        Return: 
            (List[Dict[str, str]]): list of organisation events dictionaries
        """
        with open(self.ORG_EVENTS_FILE) as f:
            return json.load(f)


    def parse_user_events(self, user_events: List[Dict[str, str]]) -> List[UserEvent]:
        """
        Description: Parse user events from file to UserEvent Objects, and ignore malformed events
        Args: 
            user_events (List[Dict[str, str]]): list of user events from file
        Return:
            (List[UserEvent]) : list of well formed user events objects
        """
        user_events_objects = []
        for user_event in user_events:
            try:
                user_event = UserEvent(**user_event)
                user_events_objects.append(user_event)
            except ValidationError as e:
                continue
                #print("MALFORMED USER EVENT IGNORED : ", user_event)
        return user_events_objects


    def parse_org_events(self, org_events: List[Dict[str, str]]) -> List[OrgEvent]:
        """
        Description: Parse organisation events from file to orgEvent Objects, and ignore malformed events
        Args: 
            org_events (List[Dict[str, str]]): list of organisation events from file
        Return:
            (List[orgEvent]) : list of well formed org events objects
        """
        org_events_objects = []
        for org_event in org_events:
            try:
                org_event = OrgEvent(**org_event)
                org_events_objects.append(org_event)
            except ValidationError as e:
                continue
                #print("MALFORMED org EVENT IGNORED : ", org_event)
        return org_events_objects


    def get_user_last_state(self, user_name: str) -> UserEvent:
        """
        Description: Fetch the last state for the provided user_name
        Args: 
            user_name (str): username
        Return:
            (UserEvent): UserEvent object that represents the user last state
        """
        users_from_file = self.read_user_events_file(self)
        users = self.parse_user_events(self, users_from_file)
        user_last_state = None
        last_state_date = ""
        for user in users:
            if user.username.lower() == user_name.lower() and user.received_at > last_state_date:
                user_last_state = user
                last_state_date = user_last_state.received_at
        return user_last_state


    def get_organisation_tier(self, organization_name: str) -> str:
        """
        Description: Fetch Organisation tier for the provided organisation name
        Args:
            organisation_name (str): organisation name
        Return:
            (str): organisation tier
        """
        if not organization_name:
            return None

        orgs_from_file = self.read_org_events_file(self)
        orgs = self.parse_org_events(self, orgs_from_file)
        org_tier = None
        for org in orgs:
            if org.organization_name == organization_name and org.organization_tier:
                org_tier = org.organization_tier
        return org_tier


    @classmethod
    def get_user_last_state_enriched(self, user_name: str) -> UserResponse:
        """
        Description: fetch the last state for the provided username with the organisation tier information
        Args:
            user_name (str): the username
        Return:
            (UserRespone): the user last state with organisation informations
        """
        user_last_state = self.get_user_last_state(
            self = self,
            user_name = user_name
        )
        
        if not user_last_state:
            return None

        user_org_tier = self.get_organisation_tier(
            self = self,
            organization_name = user_last_state.organization_name
        )
        user_last_state_enriched = UserResponse(
            username          = user_last_state.username,
            user_type         = user_last_state.user_type,
            organization_name = user_last_state.organization_name,
            organization_tier = user_org_tier
        )
        return user_last_state_enriched

    


if __name__ == "__main__":
    print(UsersService.get_user_last_state_enriched("Snake"))
    print(UsersService.get_user_last_state_enriched("M"))
    print(UsersService.get_user_last_state_enriched("Snake"))
    print(UsersService.get_user_last_state_enriched("Snake"))