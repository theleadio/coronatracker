FROM python:3.7-stretch

MAINTAINER LEAD "napster@thelead.io"

ENV HOME=/home/coronatracker

WORKDIR $HOME
RUN mkdir $HOME/app/

COPY the_star.py $HOME/app/
COPY db_connector.py $HOME/app/
COPY utils.py $HOME/app/
COPY __init__.py $HOME/app/
COPY db.json $HOME/app/
COPY requirements.txt $HOME/app/

RUN python3.7 -m pip install -r $HOME/app/requirements.txt
CMD [ "python" , "/home/coronatracker/app/the_star.py"]