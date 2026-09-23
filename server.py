import os
import sys
import json
import shutil
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DATA_FILE = os.path.join(BASE_DIR, "data_store.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/sync':
            data = load_data()
            self.send_json({"status": "live", "timestamp": datetime.now().isoformat(), "data": data})
            return

        rel_path = parsed.path.lstrip('/')
        if not rel_path or rel_path == '':
            rel_path = 'index.html'

        file_path = os.path.join(PUBLIC_DIR, rel_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            file_size = os.path.getsize(file_path)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Content-Length', str(file_size))
            if file_path.endswith('.html'):
                self.send_header('Content-Type', 'text/html; charset=utf-8')
            elif file_path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            elif file_path.endswith('.css'):
                self.send_header('Content-Type', 'text/css; charset=utf-8')
            elif file_path.endswith('.json'):
                self.send_header('Content-Type', 'application/json; charset=utf-8')
            elif file_path.endswith('.apk'):
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', 'attachment; filename="abees-baladna-v4.apk"')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            elif file_path.endswith('.png'):
                self.send_header('Content-Type', 'image/png')
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            try:
                with open(file_path, 'rb') as f:
                    shutil.copyfileobj(f, self.wfile)
            except Exception as e:
                print(f"Error serving file {file_path}: {e}")
            return

        index_path = os.path.join(PUBLIC_DIR, 'index.html')
        if os.path.exists(index_path):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            try:
                with open(index_path, 'rb') as f:
                    shutil.copyfileobj(f, self.wfile)
            except Exception as e:
                print(f"Error serving index.html: {e}")
            return

        self.send_error(404, "File not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/sync':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                new_data = json.loads(body)
                current_data = load_data()
                current_data.update(new_data)
                save_data(current_data)
                self.send_json({"status": "success", "message": "Data synchronized successfully"})
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, 400)
            return
        self.send_error(404, "Endpoint not found")

    def send_json(self, data, code=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
