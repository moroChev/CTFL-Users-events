FROM redis/redis-stack:latest


WORKDIR /events_consumer

COPY ./requirements.txt /events_consumer/requirements.txt
RUN apt-get update
RUN apt-get install python3-venv
RUN pip3 install --upgrade pip
RUN python3 -m venv venv
RUN . ./venv/bin/activate
RUN pip3 install -r /events_consumer/requirements.txt

COPY . /events_consumer

CMD [ "python", "./consume.py" ]