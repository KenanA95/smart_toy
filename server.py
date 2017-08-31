import http.server


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print("In GET function....")

    def do_POST(self):
        print("In POST function....")
