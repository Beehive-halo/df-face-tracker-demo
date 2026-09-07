import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


INDEX_HTML = b"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>DF Face Tracker</title>
  <style>
    body { margin: 0; background: #111; color: #eee; font-family: system-ui, sans-serif; text-align: center; }
    h1 { font-size: 1.1rem; font-weight: 600; margin: 14px 0 10px; }
    img { width: min(96vw, 960px); height: auto; background: #000; border-radius: 8px; }
    p { color: #aaa; font-size: .85rem; }
  </style>
</head>
<body>
  <h1>DF Face Tracker</h1>
  <img src=\"/stream.mjpg\" alt=\"Live camera stream\">
  <p>Live MJPEG camera stream</p>
</body>
</html>
"""


class _StreamHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        streamer = self.server.streamer

        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(INDEX_HTML)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(INDEX_HTML)
            return

        if self.path != "/stream.mjpg":
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Age", "0")
        self.send_header("Cache-Control", "no-cache, private")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
        self.end_headers()

        streamer._client_connected()
        last_version = -1

        try:
            while not streamer.stopped:
                frame, version = streamer.wait_for_frame(last_version)
                if frame is None:
                    continue

                last_version = version
                self.wfile.write(b"--FRAME\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(frame)}\r\n\r\n".encode())
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            streamer._client_disconnected()

    def log_message(self, format, *args):
        return


class StreamServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._condition = threading.Condition()
        self._frame = None
        self._version = 0
        self._clients = 0
        self.stopped = False

        self._server = _StreamHTTPServer((host, port), _Handler)
        self._server.streamer = self
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def has_clients(self):
        with self._condition:
            return self._clients > 0

    @property
    def client_count(self):
        with self._condition:
            return self._clients

    def start(self):
        self._thread.start()

    def publish(self, jpeg_bytes):
        with self._condition:
            self._frame = jpeg_bytes
            self._version += 1
            self._condition.notify_all()

    def wait_for_frame(self, last_version):
        with self._condition:
            self._condition.wait_for(
                lambda: self.stopped or self._version != last_version,
                timeout=2.0,
            )

            if self.stopped or self._version == last_version:
                return None, last_version

            return self._frame, self._version

    def _client_connected(self):
        with self._condition:
            self._clients += 1

    def _client_disconnected(self):
        with self._condition:
            self._clients = max(0, self._clients - 1)

    def display_url(self):
        hostname = socket.gethostname().split(".")[0]
        return f"http://{hostname}.local:{self.port}/"

    def stop(self):
        self.stopped = True
        with self._condition:
            self._condition.notify_all()
        self._server.shutdown()
        self._server.server_close()
