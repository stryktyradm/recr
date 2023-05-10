FROM python:3.11.1-slim

ADD callback_server.py /socket_app/

WORKDIR /socket_app/

ENTRYPOINT ["python3", "callback_server.py"]

CMD ["--host", "0.0.0.0"]