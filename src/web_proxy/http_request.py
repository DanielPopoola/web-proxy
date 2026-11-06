from dataclasses import dataclass
from urllib.parse import urlsplit

@dataclass(frozen=True)
class UpstreamRequest:
    host: str
    port: int
    payload: bytes


def parse_request(raw_request: bytes) -> UpstreamRequest:
    header_block, separator, _ = raw_request.partition(b"\r\n\r\n")

    if not separator:
        raise ValueError("Incomplete HTTP request headers")

    lines = header_block.decode("iso-8859-1").split("\r\n")
    method, target, version = lines[0].split(" ", 2)

    if method != "GET":
        raise ValueError("Only GET requests are supported")

    if version not in ("HTTP/1.0", "HTTP/1.1"):
        raise ValueError("Unsupported HTTP version")

    if target.startswith("http://"):
        url = urlsplit(target)
        host = url.hostname
        port = url.port or 80
        path = url.path or "/"

        if url.query:
            path += f"?{url.query}"

    else:
        host_header = next(
            (
            line.split(":", 1)[1].strip()
            for line in lines[1:]
            if line.lower().startswith("host:")
            ),
            None,
        )

        if not host_header:
            raise ValueError("Missing Host header")

        url = urlsplit(f"http://{host_header}")
        host = url.hostname
        port = url.port or 80
        path = target

    if not host:
        raise ValueError("Missing destination hostname")

    forwarded_lines = [
        f"{method} {path} {version}",
        *[
            line
            for line in lines[1:]
            if not line.lower().startswith("proxy-connection:")
            and not line.lower().startswith("connection:")
        ],
        "Connection: close",
        "",
        "",
    ]

    payload = "\r\n".join(forwarded_lines).encode("iso-8859-1")

    return UpstreamRequest(
        host=host,
        port=port,
        payload=payload
    )