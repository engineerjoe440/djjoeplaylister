# Dockerfile for DJJoe Calendar App
FROM python:3.11

WORKDIR /server

COPY ./requirements.txt /server

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./app /server

# Run Server on localhost:8383 so Nginx can Hit it without Direct Extern. Access
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "log_conf.yml"]