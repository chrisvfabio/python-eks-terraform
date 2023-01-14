# Kubernetes hello-world

This hello-world app has 2 endpoints:
- '/' which displays an "Hello World!" message with the name of the pod it runs
    into and its current version. It also performs heavy computations every time it is accessed.
- '/health' which provides a basic health check

# Installation

This application is a Python app. It runs smoothly in Python 3.5 and Python 2.7.
To run it, you will need to install its dependencies first:
```
pip install -r ./requirements.txt
```
Then you will be able to launch it:
```
python ./app.py
```
By default, the app listens on port *5000*.

This application can also be served by Passenger + Nginx using WSGI without any change in the code.
