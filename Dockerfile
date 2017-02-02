FROM python:3.6-alpine

WORKDIR /srv
ADD . /srv
RUN pip install -q -r /srv/requirements.txt
CMD ["/srv/run.py"]

