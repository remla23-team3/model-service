FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app
COPY README.md /app

RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt

COPY src/ /app

EXPOSE 6789

ENTRYPOINT ["python"]
CMD ["app.py"]
