# flask_boilerplate


This project will serve as a template when creating web services. There are two ways to stand of the flask app

clone the repo on to a location on your drive

setup virtual environment
```` shell
pip freeze > .\requirements.txt
````
```` shell
python server.py
````
or

Download the docker image
```` shell
docker pull peezus/flask_boilerplate
````
run the image
```` shell
docker run -d -p 5000:5000 --name service-name peezus/flask_boilerplate:0.1.0
````