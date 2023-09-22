FROM python:3.8-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001
COPY src .
CMD [ "python", "run.py" ]
