# Web Proxy

A multithreaded HTTP proxy server implemented in Python. The proxy accepts HTTP requests from clients, forwards them to origin servers, and relays the responses back to the clients.

This project is an implementation of the multithreaded web proxy assignment from *Computer Networking: A Top-Down Approach*. It explores TCP sockets, HTTP request forwarding, concurrency, and network resource management.

## Features

- **HTTP request forwarding:** Receives HTTP GET requests and forwards them to the appropriate origin server.
- **Response relaying:** Returns origin server responses to the requesting client.
- **Multithreading:** Handles client connections using separate worker threads.
- **Modular architecture:** Separates connection handling, HTTP request parsing, upstream communication, and server management.
- **Error handling:** Handles malformed requests and connection errors with basic HTTP error responses.
- **Connection cleanup:** Uses socket context managers to close connections and release resources.

## Requirements

- Python 3.12 or later (adjust this to match `requires-python` in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) for project and environment management

## Project Structure

```text
web-proxy/
├── README.md
├── pyproject.toml
├── proxy.py
└── src/
    └── web_proxy/
        ├── __init__.py
        ├── __main__.py
        ├── server.py
        ├── handler.py
        ├── http_request.py
        └── upstream.py
```

| Module | Responsibility |
|---|---|
| `server.py` | Creates the listening socket and dispatches client connections to worker threads. |
| `handler.py` | Coordinates the lifecycle of an individual client request and handles errors. |
| `http_request.py` | Parses HTTP requests and extracts the origin server's hostname, port, and request payload. |
| `upstream.py` | Connects to origin servers, forwards requests, and relays responses. |
| `__main__.py` | Enables execution using `python -m web_proxy`. |
| `proxy.py` | Provides a root-level entry point for running the proxy. |

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/DanielPopoola/web-proxy
cd web-proxy
```

Install the project and its dependencies:

```bash
uv sync
```

This project currently uses Python's standard library for networking and concurrency.

## Usage

Start the proxy:

```bash
uv run web-proxy
```

Alternatively, run it as a Python module:

```bash
uv run python -m web_proxy
```

By default, the proxy listens on:

```text
127.0.0.1:8888
```

The host and port can be configured in `src/web_proxy/server.py`.

### Configure a client

Configure an HTTP client to use the proxy at `127.0.0.1:8888`.

For example, using `curl`:

```bash
curl --proxy http://127.0.0.1:8888 http://example.com/
```

The proxy receives the request, connects to the origin server, forwards the request, and relays the response to `curl`.

The example above uses plain HTTP. HTTPS requests require additional support for the `CONNECT` method and are not supported by the current implementation.

## How It Works

1. The server creates a TCP listening socket and waits for incoming client connections.
2. When a client connects, the server starts a worker thread to handle that connection.
3. The request handler reads the client's HTTP request and passes it to the request parser.
4. The parser extracts the destination hostname, port, and request payload.
5. The upstream module establishes a TCP connection to the origin server and forwards the request.
6. The origin server returns an HTTP response, which the proxy relays to the client.
7. The connections are closed when the request finishes or an error occurs.

Each worker handles its own client connection, allowing multiple requests to make progress concurrently.

## Current Limitations

This is an educational implementation, not a production-ready proxy.

- Supports HTTP GET requests only.
- Does not support HTTPS tunnelling or the `CONNECT` method.
- Reads only an initial, fixed-size chunk of the client request; requests with headers larger than that chunk or headers split across TCP reads may fail.
- Uses a thread-per-connection model without a bounded worker pool.
- Does not implement response caching or connection pooling.
- Has basic timeout and error handling.
- Does not yet comprehensively validate HTTP syntax, message framing, or all header requirements.
- Does not implement authentication, access controls, or production-grade logging.

Do not expose this proxy to untrusted networks. Its current design is intended for controlled, local experimentation.

## Learning Objectives

This project provides practical experience with:

- TCP sockets and client-server communication.
- HTTP request and response structure.
- Forward proxies and origin servers.
- Concurrent connection handling with Python threads.
- Socket timeouts and resource cleanup.
- Separation of concerns and modular software design.
- The limitations of blocking I/O and thread-per-connection concurrency.

## Future Improvements

Potential extensions include:

- Read HTTP headers incrementally with a maximum header-size limit.
- Add unit tests for URL parsing, malformed requests, and destination extraction.
- Add integration tests for request forwarding and response correctness.
- Test concurrent clients using deliberately slow origin servers.
- Introduce a bounded thread pool to limit resource consumption.
- Improve timeout handling and error reporting.
- Add support for additional HTTP methods and HTTPS tunnelling.
- Measure throughput and response latency under concurrent load.

## License

No license has been specified yet. Add a license file if you intend to distribute or reuse this project publicly.
