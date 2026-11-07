from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
class AtlasHandler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path.split('?')[0]=='/':self.path='/California-Rail-Atlas.html'
  super().do_GET()
 def end_headers(self):
  self.send_header('Cache-Control','no-cache')
  super().end_headers()
print('California Rail Atlas is ready on port 3000',flush=True)
ThreadingHTTPServer(('0.0.0.0',3000),AtlasHandler).serve_forever()
