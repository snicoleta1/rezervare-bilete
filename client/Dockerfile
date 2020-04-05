FROM python:3.6

EXPOSE 5005

WORKDIR /client

COPY requirements.txt /client
RUN pip3 install -r requirements.txt

COPY client.py /client
CMD python3 client.py
