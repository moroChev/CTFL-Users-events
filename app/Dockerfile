FROM python:3.9


WORKDIR /cftl_challenge

COPY ./requirements.txt /cftl_challenge/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /cftl_challenge/requirements.txt
RUN mkdir /cftl_challenge/app

COPY . /cftl_challenge/app