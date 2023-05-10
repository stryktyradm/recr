import socket
import argparse
from urllib.parse import urlparse, parse_qsl
import selectors

URLS = ["/"]


def parse_args():
    parser = argparse.ArgumentParser(description="Set the address to start the server")

    parser.add_argument(
        "--host",
        type=str,
        required=True,
        help="host IP-address"
    )

    return parser.parse_args()


def parse_request(request):
    parsed = request.decode().split(" ")
    method = parsed[0]
    parsed_url = urlparse(parsed[1])
    url_path, query_string = parsed_url.path, parse_qsl(parsed_url.query)
    return method, url_path, dict(query_string)


def generate_headers(method, url):
    if not method == "GET":
        return "HTTP/1.1 405 Method not allowed\nConnection: close\n\n", 405
    if url not in URLS:
        return "HTTP/1.1 404 Not found\nConnection: close\n\n", 404
    return "HTTP/1.1 200 OK\nConnection: close\n\n", 200


def generate_content(code, query_string):
    if code == 404:
        return "<h1>404</h1><p>Not Found!</p>"
    if code == 405:
        return "<h1>405</h1><p>Method not allowed!</p>"
    return f"<h1>Hello, {query_string.get('name', 'Anon')}! </h1>" \
           f"<h2>{query_string.get('message', ':(')}</h2>"


def generate_response(request):
    method, url, query_string = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, query_string)
    return (headers + body).encode("utf-8")


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    client_socket.setblocking(False)
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message)


def send_message(client_socket):
    request = client_socket.recv(1024)
    if request:
        response = generate_response(request)
        client_socket.send(response)
        selector.unregister(client_socket)
        client_socket.close()
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = selector.select(timeout=1)
        for event, _ in events:
            callback = event.data
            callback(event.fileobj)


if __name__ == "__main__":

    selector = selectors.DefaultSelector()
    args = parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setblocking(False)
        server_socket.bind((args.host, 80))
        server_socket.listen(10)
        print(f"Start server on socket: {args.host}:{80}")
        selector.register(fileobj=server_socket,
                          events=selectors.EVENT_READ,
                          data=accept_connection)

        event_loop()
