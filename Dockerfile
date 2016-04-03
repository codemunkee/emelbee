FROM ubuntu:latest
MAINTAINER Russ
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /emelbee
WORKDIR /emelbee
RUN pip install -r requirements.txt
RUN python setup.py install
ENTRYPOINT ["python"]
CMD ["/emelbee/bin/emelbee_api"]
