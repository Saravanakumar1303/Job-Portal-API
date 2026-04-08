FROM python:3.12-bullseye

ENV IS_DOCKER_BUILD="1"
ENV HOME="/root"
ENV PROJECT_DIR="/app"

WORKDIR ${PROJECT_DIR}

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install -U setuptools

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]