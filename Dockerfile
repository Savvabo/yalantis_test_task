FROM tiangolo/uwsgi-nginx-flask:python3.8
#RUN apt-get --update add bash nano
#WORKDIR /app

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
ENTRYPOINT python -m unittest tests/* > tests.log 2>&1 && python main.py > api.log 2>&1
