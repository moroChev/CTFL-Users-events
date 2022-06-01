import json
import time
import random
from utils import UserEvent, OrgEvent
from utils import get_user_events_parsed, get_org_events_parsed, get_container_ip_address
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, KafkaConfigurationError



def serializer(message):
    return json.dumps(message).encode('utf-8')


class ProducerService():

    producer: KafkaProducer = None
    
    USERS_TOPIC = "users-events"
    ORGS_TOPIC  = "orgs-events"
    CONFIG      = {
        "bootstrap_servers": ["localhost:9092"],
        "value_serializer": serializer,
        "key_serializer": serializer
    }



    def _create_producer(self) -> None:
        try:
            self.producer = KafkaProducer(**self.CONFIG)
        except Exception as e:
            print(e)


    def _close_producer(self) -> None:
        try:
            self.producer.close()
            print("PRODUCER CLOSED")
        except Exception as e:
            print("COULDN't CLOSE PRODUCER ", e)
            

    def _publish_user_event(self, user_event: UserEvent) -> None:
        try:
            self.producer.send(
                self.USERS_TOPIC, 
                key=user_event.user_id,
                value=user_event.dict()
            )
            print(f"SEND USER EVENT : {user_event}")
        except KafkaTimeoutError as e:
            print(f"UNABLE TO SEND USER EVENT : {user_event} , ERROR {e}")


    def _publish_org_event(self, org_event: OrgEvent) -> None:
        try: 
            self.producer.send(
                self.ORGS_TOPIC, 
                key=org_event.organization_key,
                value=org_event.dict()
            )
            print(f"SENT ORG EVENT : {org_event}")
        except KafkaTimeoutError as e:
            print(f"UNABLE TO SEND ORG EVENT : {org_event} , ERROR {e}")


    @classmethod
    def produce(self):
        self._create_producer(self)
        users_events = get_user_events_parsed()
        orgs_events  = get_org_events_parsed()
        nbr_users_events = len(users_events)
        nbr_orgs_events  = len(orgs_events)
        max_len = max(nbr_orgs_events, nbr_users_events)
        try:
            for i in range(max_len):
                if i < nbr_orgs_events:
                    org_event = orgs_events[i]
                    self._publish_org_event(self, org_event)

                if i < nbr_users_events:
                    user_event = users_events[i]
                    self._publish_user_event(self, user_event)

                time_to_sleep = random.randint(1, 2)
                time.sleep(time_to_sleep)
            print("FINISH PRODUCING")
        except Exception as e:
            print(e)
        finally:
            self._close_producer(self)
            
    



if __name__ == "__main__":
   print(f"WAIT ------> 10 = FOR BROKER TO BE READY {ProducerService.CONFIG}")
   #time.sleep(10)
   print("Start Producing")
   ProducerService.produce()


