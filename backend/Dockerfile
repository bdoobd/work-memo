FROM python:3.12-alpine

WORKDIR /backend

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090", "--reload" ]