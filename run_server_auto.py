import socketserver
import http.server
import os
import sys

PORT = 8089
DIRECTORY = 'dist'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        # Override to return text/html for extensionless files
        base, ext = os.path.splitext(path)
        if not ext:
            return 'text/html'
        return super().guess_type(path)

# Try to find an available port
while True:
    try:
        with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
            print(f'Serving at port {PORT}')
            httpd.serve_forever()
            break
    except OSError as e:
        if e.errno == 10048:
            print(f"Port {PORT} is in use, trying next port...")
            PORT += 1
        else:
            raise
