FROM python:3.7

MAINTAINER Andrew Slesarenko <swen295@gmail.com>

COPY . /opt/app/marky
RUN pip3 install -r /opt/app/swen_tech/requirements.txt
WORKDIR /opt/app/marky

ENTRYPOINT ["python3", "run.py"]