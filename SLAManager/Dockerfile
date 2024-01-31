FROM python:3.10
WORKDIR /usr/src/SLAManager
COPY ./ /usr/src/SLAManager
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]