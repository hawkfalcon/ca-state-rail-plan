from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

class AtlasHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?', 1)[0] == '/':
            self.path = '/index.html' if (ROOT / 'index.html').exists() else '/California-Rail-Atlas.html'
        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    print('California Rail Atlas is ready on port 3000', flush=True)
    ThreadingHTTPServer(('0.0.0.0', 3000), AtlasHandler).serve_forever()
