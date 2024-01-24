FROM python:3.10
WORKDIR /usr/src/MeteoRetrieval
COPY ./ /usr/src/MeteoRetrieval
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]


ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=wdb
ENV MYSQL_USER=wnotif
ENV MYSQL_PASSWORD=wnotif