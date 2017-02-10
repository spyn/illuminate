#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import os
from fx import *


with open('config.json', 'r') as f:
    config = json.load(f)

with open('effects.json', 'r') as f:
    effects = json.load(f)

web_port = config['port']
run_path = os.path.dirname(os.path.realpath(__file__))


class my_web(BaseHTTPRequestHandler):
  
  def do_GET(self):

    client = self.client_address
    client_ip = client[0]
    if '10.1.1.' not in client_ip:
      self.send_error(302, 'Nah')

    if self.path == '/':
      self.path = '/index.html'

    uri = self.path.split("/")

    if self.path == '/devices' or self.path == '/effects' or self.path == '/bulbs':
      content = None
      if self.path == '/devices':
        content = json.dumps(config['devices'])
      if self.path == '/effects':
        content = json.dumps(effects)
      if self.path == '/bulbs':
        content = discover_yeebulbs()
        
      if content is not None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(content)

      if content is None:
        self.send_error(404,'File Not Found')
      return

    if len(uri) == 2:
      print self.path
      try: 
        content = None
        sendReply = False
        if self.path.endswith(".html"):
          mimetype='text/html'
          sendReply = True
        if self.path.endswith(".js"):
          mimetype='application/javascript'
          sendReply = True
        if self.path.endswith(".css"):
          mimetype='text/css'
          sendReply = True
        if ".." in self.path:
          sendReply = False

        if sendReply:
          f = open(run_path + "/static" + self.path)
          self.send_response(200)
          self.send_header('Content-type', mimetype)
          self.end_headers()
          self.wfile.write(f.read())
          f.close()
        return
      except IOError:
        self.send_error(404,'File Not Found')

    if len(uri) == 3 or len(uri) == 4:

      dev = uri[1]
      cmd = uri[2]

      if dev == None or cmd == None:
        self.send_error(403,'Computer says no')

      if dev and cmd:
        wegood = False
        if 'yee-both' in dev:
          yees = []
          for device in config['devices']:
            if 'yeelight' in device.type:
              yees.append(device)
          event_yeelight_both(yees)
          wegood = True

        for device in config['devices']:
          if dev == device['alias']:
            if 'hyperion' == device['type']:
              for effect in effects['hyperion']:
                if effect['name'] == cmd:
                  event_hyperion(device, effect)
                  wegood = True
            if 'yeelight' == device['type']:
              for effect in effects['yeelight']:
                if effect['name'] == cmd:
                  event_yeelight(device, effect)
                  wegood = True

      if wegood:
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("OK")
        return
      if wegood == False:
        self.send_error(404,'Unable to light this shit up')
        return

    self.send_error(400,'Negative Ghostrider')

try:
  server = HTTPServer(('', web_port), my_web)
  print '[*] Started illuminate on localhost:' + str(web_port)
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()




