FROM python:3.8.5
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY secure_config.sh .

COPY ./backend ./backend

CMD bash -c 'source secure_config.sh; cd backend; python app.py'

