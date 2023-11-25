FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN apt-get update
RUN sh -c '/bin/echo' -e "y" | apt-get install python3-pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]