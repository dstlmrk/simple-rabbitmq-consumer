FROM python:3.12.0-slim

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY /src/service/ /service
CMD ["python", "-u", "/service/main.py"]
