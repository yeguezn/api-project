FROM python:3.10

WORKDIR /app

ENV SECRET_KEY 40oKXLIE-DTWePp-9186hw

ENV DB_NAME api_auth

ENV MONGODB_SERVER db

RUN \ 
    echo "SECRET_KEY=$SECRET_KEY" > .env && \ 
    echo "DB_NAME=$DB_NAME" >> .env && \ 
    echo "MONGODB_SERVER=$MONGODB_SERVER" >> .env

COPY . .

RUN pip install -r requirements.txt

CMD python app.py
