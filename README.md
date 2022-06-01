# Introduction

The following is an implementation of an API to fetch last state of users events.

# Project Setup

### Prerequisites

- Python 3.8.6 or higher
- FastAPI
- Docker

### Running the API with the Docker Container

- We have the Dockerfile created in above section. Now, we will use the Dockerfile to create the image of the FastAPI app and then start the FastAPI app container.
- Using a preconfigured `Makefile` tor run the Docker Compose:

```sh
# Pull the latest image
$ make pull

# Build the image
$ make build

# Run the containers
$ make start

# start producing data
$ make produce
```


```

# Project Structure

```sh
.
├── app
│   ├── __init__.py
│   ├── main.py                # contains the api end point
│   ├── service.py             # contains the api business logic
│   ├── Dockerfile.py          # dockerfile for redis container
│   ├── utils.py               # contains some common elements  
│   └── requirements.txt       # the env requirements
│ 
├── redis
│   ├── consume.py                # data consumer
│   ├── Dockerfile.py             # dockerfile for redis container
│   ├── requirements.txt          # the env requirements
│   └── utils.py                  # contains some common elements
│ 
├── producer
│   ├── __init__.py
│   ├── produce.py                # script to produce data
│   ├── utils.py                  # contains some common elements
│   └── data/ 
│        ├── org_events.json       # org events data  
│        └── user_events.json      # users events data   
│           
├── docker-compose.yaml
├── Makefile
└── requirements.txt
```
