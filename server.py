import http.server


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
    # Parse out the command and value from the POST
    command = post_data.split('=')[0]
    val = post_data.split('=')[1]

    if command == 'f':
        print("Forward ", val)
    elif command == 'b':
        print("Backward ", val)
    elif command == 'l':
        print("Left  ", val)
    elif command == 'r':
        print("Right  ", val)
    else:
        print("Invalid Command: ", command)


def run_server(port, server_class=http.server.HTTPServer, handler_class=ToyHandler):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Serving PORT: ", port)
    httpd.serve_forever()

run_server(port=8000)
