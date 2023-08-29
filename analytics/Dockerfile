FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /analytics
COPY . /analytics/

# install system dependencies
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y netcat

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /analytics/entrypoint.sh
RUN chmod +x /analytics/entrypoint.sh


# run entrypoint.sh
ENTRYPOINT ["/analytics/entrypoint.sh"]