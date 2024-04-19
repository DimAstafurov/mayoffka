FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN mkdir /api-app

WORKDIR /api-app

COPY ./requirements.txt /api-app/requirements.txt

COPY ./api .

RUN pip install --no-cache-dir --upgrade -r /api-app/requirements.txt