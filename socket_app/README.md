**Simple HTTP-server based on socket interface.**

Run in docker container:

```shell
docker build -f ./Dockerfile -t socket_server:latest .
```

```shell
docker run -d --name socket_server -p 80:80/tcp socket_server:latest
```

Run as python script:

```shell
python3 callback_server.py --host 0.0.0.0
```