import http.server
import urllib
import json

PORT = 8000


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print("In GET function....")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        print("In POST function....")
        self.send_response(200)
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        forward_command(post_data)


# Forward the message along to the hardware side. For now just print out a message to console
def forward_command(post_data):
    post_arg = post_data.split('=')[0]
    val = post_data.split('=')[1]

    if post_arg == 'f':
        print("Forward ", val)
    elif post_arg == 'b':
        print("Backward ", val)
    elif post_arg == 'l':
        print("Left  ", val)
    elif post_arg == 'r':
        print("Right  ", val)
    else:
        print("Invalid Command: ", post_arg)


def run(server_class=http.server.HTTPServer, handler_class=ToyHandler):

    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)

    print("Serving PORT: ", PORT)
    httpd.serve_forever()

run()