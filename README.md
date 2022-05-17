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

# Run the container
$ make start
```


### Running the API locally

- In case we do not have Docker already instaled, we can run the API in our local environment by executing the following commands.


```sh
# creating virtual environment
$ python3 -m venv venv

# activate virtual environment
$ source venv/bin/activate

# install all dependencies
$ pip install -r requirements.txt

# Running the application using uvicorn
$ uvicorn app.main:app --reload
```

# Project Structure

```sh
.
├── app
│   ├── __init__.py
│   ├── main.py                # contains the api end point
│   ├── service.py             # contains the api business logic
│   ├── utils.py               # contains some common elements
│   └── data/ 
│        ├── org_events.json       # org events data  
│        └── user_events.json      # users events data   
│           
├── Dockerfile
├── docker-compose.yaml
├── Makefile
└── requirements.txt
```
