FROM python:3.8-slim-buster
ARG PAT_TOKEN=''
WORKDIR /app    
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=${PAT_TOKEN}
COPY . /app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "src/server.py" ]