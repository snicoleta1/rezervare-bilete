FROM python:latest

EXPOSE 5000

WORKDIR /server

COPY requirements.txt /server
RUN pip3 install -r requirements.txt

COPY server.py /server
CMD python3 server.py
