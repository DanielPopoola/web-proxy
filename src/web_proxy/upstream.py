from socket import AF_INET, SOCK_STREAM, socket

from web_proxy.http_request import UpstreamRequest

BUFFER_SIZE = 4096
UPSTREAM_TIMEOUT = 10

def forward_request(client_socket: socket, request: UpstreamRequest) -> None:
    with socket(AF_INET, SOCK_STREAM) as origin_socket:
        origin_socket.settimeout(UPSTREAM_TIMEOUT)
        origin_socket.connect((request.host, request.port))
        origin_socket.sendall(request.payload)

        while True:
            data = origin_socket.recv(BUFFER_SIZE)
            if not data:
                break

            client_socket.sendall(data)