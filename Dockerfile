FROM python:3.10

WORKDIR /app
EXPOSE 5000

ENV FLASK_DEBUG 1

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

# docker run -p 5000:5000 -v ${PWD}:/app flask-rest-api