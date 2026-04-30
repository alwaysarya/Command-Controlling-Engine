"""
CMD ENGINE - Phone Server (Windows)
HTTP server that receives commands from your phone.
Serves the phone web interface and processes commands.
"""

import json
import sys
import os
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.brain import quick_parse
from core.executor import run as execute
from core.memory import remember_command
from outputs.speak import say


# Hard-coded path to the phone folder
PHONE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phone")


class PhoneHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Suppress HTTP log spam."""
        pass

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _serve_file(self, filepath, content_type):
        if os.path.exists(filepath):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/status":
            self._send_json({
                "status": "online",
                "engine": "CMD ENGINE",
                "version": "1.0",
                "platform": "windows"
            })

        elif self.path == "/" or self.path == "/index.html":
            self._serve_file(os.path.join(PHONE_DIR, "index.html"), "text/html")

        elif self.path == "/style.css":
            self._serve_file(os.path.join(PHONE_DIR, "style.css"), "text/css")

        elif self.path == "/app.js":
            self._serve_file(os.path.join(PHONE_DIR, "app.js"), "application/javascript")

        elif self.path == "/manifest.json":
            self._serve_file(os.path.join(PHONE_DIR, "manifest.json"), "application/json")

        elif self.path == "/sw.js":
            self._serve_file(os.path.join(PHONE_DIR, "sw.js"), "application/javascript")

        elif self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()

        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path == "/command":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length == 0:
                    self._send_json({"error": "Empty request"}, 400)
                    return

                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)
                command = data.get("command", "").strip()

                if not command:
                    self._send_json({"error": "No command provided"}, 400)
                    return

                print(f"\n📱 Phone command: {command}")

                action = quick_parse(command)
                print(f"🧠 Action: {action}")

                result = execute(action)
                print(f"⚡ Result: {result}")

                remember_command(command, result, action)

                try:
                    say(result)
                except:
                    pass

                self._send_json({
                    "command": command,
                    "action": action,
                    "result": result
                })

            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, 400)
            except Exception as e:
                print(f"❌ Server error: {e}")
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "Not found"}, 404)


def get_local_ip():
    """Get the local network IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def start_server(port=9999):
    """Start the HTTP server."""
    ip = get_local_ip()

    print(f"""
    ╔══════════════════════════════════════════╗
    ║     CMD ENGINE - Phone Server Ready      ║
    ╠══════════════════════════════════════════╣
    ║                                          ║
    ║  📱 Local:  http://{ip}:{port}        ║
    ║  📱 Alt:    http://localhost:{port}      ║
    ║                                          ║
    ║  Open this URL on your phone browser      ║
    ║  Phone and PC must be on same network      ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
    """)

    try:
        server = HTTPServer(("0.0.0.0", port), PhoneHandler)
        print(f"🚀 Server listening on port {port}...\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
        server.shutdown()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {port} is already in use.")
        else:
            print(f"\n❌ Server error: {e}")


if __name__ == "__main__":
    print(f"Your PC IP: {get_local_ip()}")
    start_server()