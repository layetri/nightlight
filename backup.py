import time
from gpiozero import RGBLED
from colorzero import Color
import socket
import socketserver
import datetime
from http import server

running = False
led = RGBLED(26, 6, 5, active_high=True, initial_value=Color(130, 200, 40))
blinking = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

PORT = 8000
Handler = server.SimpleHTTPRequestHandler


def run():
    with socketserver.TCPServer((ip, PORT), Handler) as httpd:
        def do_GET(self):
            if self.path == '/':
                self.path = '/index.html'
            elif self.path == 'on':
                led.on()
                self.path = '/index.html'
            elif self.path == 'off':
                led.off()
                self.path = '/index.html'
            elif self.path == '/date':
                do_time(self)
            return server.SimpleHTTPRequestHandler.do_GET(self)

        print(time.asctime(), 'Server UP - %s:%s' % (ip, PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print(time.asctime(), 'Server DOWN - %s:%s' % (ip, PORT))


def do_time(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("<b> Hello World !</b>"
                     + "<br><br>Current time: " + str(datetime.datetime.now()))


while 1:
    command = input(" -> ")

    if command == 'start':
        run()
    elif command == 'quit':
        exit()