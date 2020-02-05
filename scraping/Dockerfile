FROM python:3.7-stretch

MAINTAINER LEAD "napster@thelead.io"

ENV HOME=/home/coronatracker

WORKDIR $HOME
RUN mkdir $HOME/coronatracker

COPY TheStar.py $HOME/
COPY db_connector.py $HOME/
COPY db.json $HOME/
COPY requirements.txt $HOME/

RUN python3.7 -m pip install -r $HOME/requirements.txt
CMD [ "python" , "/home/coronatracker/TheStar.py"]