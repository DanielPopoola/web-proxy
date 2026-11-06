from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, socket
from threading import Thread

from web_proxy.handler import handle_client


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8888
BACKLOG = 20


def main():
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((DEFAULT_HOST, DEFAULT_PORT))
        server_socket.listen(BACKLOG)

        print(f"Proxy listening on {DEFAULT_HOST}:{DEFAULT_PORT}")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            worker = Thread(
                target=handle_client,
                args=(client_socket,),
                daemon=True
            )
            worker.start()


if __name__ == "__main__":
    main()