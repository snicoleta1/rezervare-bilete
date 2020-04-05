FROM python:3.6

EXPOSE 5010

WORKDIR /admin

COPY requirements.txt /admin
RUN pip3 install -r requirements.txt

COPY admin.py /admin
CMD python3 admin.py
