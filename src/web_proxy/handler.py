from socket import socket

from web_proxy.http_request import parse_request
from web_proxy.upstream import forward_request


def handle_client(client_socket: socket) -> None:
    with client_socket:
        try:
            client_socket.settimeout(10)
            raw_request = client_socket.recv(4096)
            if not raw_request:
                return
            
            request = parse_request(raw_request)
            forward_request(client_socket, request)

        except ValueError as error:
            print(f"Invalid request: {error}")
            _send_error(client_socket, 400, "Bad Request")

        except OSError as error:
            print(f"Proxy connection error: {error}")
            _send_error(client_socket, 502, "Bad Gateway")

def _send_error(client_socket: socket, status_code: int, reason: str) -> None:
    response = (
        f"HTTP/1.1 {status_code} {reason}\r\n"
        "Connection: close\r\n"
        "Content-Length: 0\r\n"
        "\r\n"
    )

    try:
        client_socket.sendall(response.encode("ascii"))
    except OSError:
        pass