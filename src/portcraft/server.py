import json

from http.server import HTTPServer, BaseHTTPRequestHandler


class GitHubWebhookHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler to process GitHub webhooks."""

    def do_GET(self):
        print(f"Received GET request from {self.client_address}")
        print("Headers:")
        for header, value in self.headers.items():
            print(f"{header}: {value}")

        content_length = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Received successfully")



    def do_POST(self):
        # Log the incoming request
        print(f"Received POST request from {self.client_address}")

        # Get the headers
        print("Headers:")
        for header, value in self.headers.items():
            print(f"{header}: {value}")

        # Determine content length
        content_length = int(self.headers.get('Content-Length', 0))

        # Read and decode the payload
        payload = self.rfile.read(content_length).decode('utf-8')
        print("\nPayload:")
        try:
            # Parse JSON payload
            payload_json = json.loads(payload)
            print(json.dumps(payload_json, indent=4))
        except json.JSONDecodeError:
            print("Payload is not valid JSON, its in urlencoded string")
            print(payload)

        # Respond with a 200 OK
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Webhook received successfully")


def run(server_class=HTTPServer, handler_class=GitHubWebhookHandler):
    """Starts the HTTP server."""
    server_address = ("0.0.0.0", 8000)
    print(f"Starting server at http://{server_address[0]}:{server_address[1]}")
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run()
