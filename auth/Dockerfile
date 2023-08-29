FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /auth
COPY . /auth/

# install system dependencies
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y netcat

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /auth/entrypoint.sh
RUN chmod +x /auth/entrypoint.sh


# run entrypoint.sh
ENTRYPOINT ["/auth/entrypoint.sh"]