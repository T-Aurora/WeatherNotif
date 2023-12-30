FROM python:3.10
WORKDIR /usr/src/WNotif
COPY ./ /usr/src/WNotif
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]


ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=wdb
ENV MYSQL_USER=wnotif
ENV MYSQL_PASSWORD=wnotif

