from enum import Enum
from typing import List
from utils import UserEvent, OrgEvent, UserLastState, parse_user_event, parse_org_event
from kafka import KafkaConsumer
from redis_om.model import NotFoundError
from redis_om import Migrator
import json


def deserializer(message: str):
    return json.loads(message.decode('ascii'))


class Topic(Enum):
    USERS = "users-events"
    ORGS  = "orgs-events"


class ConsumerService(object):

    TOPICS = ["users-events", "orgs-events"]
    CONFIG = {
            "bootstrap_servers":'kafka:9092',
            "value_deserializer" : deserializer,
            "auto_offset_reset": 'earliest',
            "enable_auto_commit": True,
            "auto_commit_interval_ms": 1000
        }
    consumer: KafkaConsumer = None


    def _create_consumer(self) -> None:
        """ creating the kafka consumer """
        try:
            self.consumer = KafkaConsumer(**self.CONFIG)
            print("CONSUMER CREATED")
        except Exception as e:
            print(e)


    def _get_user_by_id(user_id: str) -> UserLastState:
        """
        Description: get the last saved state for a user based on the user id
        Params:
            user_id (str): the user id
        Returns:
            (serLastState): the user last saved state if found 
        """
        try:
            user = UserLastState.find(UserLastState.user_id == user_id).all()
            if user:
                return user[0]
        except Exception as e: 
            print(f"UNFOUND USER ID : {user_id} ", e)
            return None


    def _get_users_by_org_name(org_name: str) -> List[UserLastState]:
        """
        Description: get the last saved state for a user based on the user id
        Params:
            user_id (str): the user id
        Returns:
            (UserEvent): the user last saved state if found 
        """
        try:
            users = UserLastState.find(UserLastState.organization_name == org_name).all()
            return users
        except Exception as e: 
            print(f"No User with org name : {org_name} ", e)
            return None
    

    def _update_state_with_user_infos(self, user_event: UserEvent) -> None:
        try:
            user_last_save = self._get_user_by_id(user_event.user_id)

            if user_last_save:
                if user_event.received_at > user_last_save.received_at:
                    print(f"{user_last_save} WILL GET UPDATED")
                    user_last_save.username  = user_event.username
                    user_last_save.user_type = user_event.user_type
                    user_last_save.received_at = user_event.received_at
                print(f"USER STATE UPDATED WITH USER INFOS {user_last_save}")
            else:
                new_user = UserLastState(**user_event.dict())
                new_user.save()
                print(f"ADD {new_user} FIRST TIME")
        except Exception as e:
            print(e)


    def _update_state_with_org_infos(self, org_event: OrgEvent) -> None:
        try:
            users_last_save = self._get_users_by_org_name(org_name = org_event.organization_name)
            if users_last_save:
                for user in users_last_save:
                    user.organization_name  = org_event.organization_name
                    user.organization_key   = org_event.organization_key
                    user.organization_tier  = org_event.organization_tier
                    user.save()
                    print(f"USER STATE UPDATED WITH ORG INFOS {user}")
        except Exception as e:
            print(e)


    @classmethod
    def consume(self):
        print("START CONSUMING")
        try:
            self._create_consumer(self)
            self.consumer.subscribe(topics=self.TOPICS)
            Migrator().run()
            for msg in self.consumer:
                if msg.topic == Topic.USERS.value:
                    print("---> USER EVENT")
                    user_event = parse_user_event(msg.value)
                    if user_event:
                        self._update_state_with_user_infos(self, user_event)
                elif msg.topic == Topic.ORGS.value:
                    print("---> ORG EVENT")
                    org_event = parse_org_event(msg.value)
                    if org_event:
                        self._update_state_with_org_infos(self, org_event)
        except Exception as e:
            print(e)
        finally:
            self.consumer.close()

    


if __name__ == "__main__":
    ConsumerService.consume()

