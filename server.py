import http.server

PORT = 8000


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print("In GET function....")

    def do_POST(self):
        print("In POST function....")


def run(server_class=http.server.HTTPServer, handler_class=ToyHandler):

    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)

    print("Serving PORT: ", PORT)
    httpd.serve_forever()

