import http.server
from record_route import *
from datetime import datetime


# State variable to keep track if the route requests should be recorded for playback
record = Record()


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_GET(self):
        print("In GET function...")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        length = int(self.headers['Content-Length'])
        value = self.rfile.read(length).decode('utf-8')
        debug_statement_post(self.path, value)
        handle_request(self.path, value)


# temp functions
def debug_statement_post(path, value):
    print("In POST function...")
    print("Path sent to: {0}".format(path))
    print("Value received {0}".format(value))


def run_server(port):

    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, ToyHandler)
    print("Serving PORT: ", port)
    httpd.serve_forever()


def handle_request(path, value):

    if path == '/forwardBack' or path == '/leftRight':
        send_to_hardware(command=path, val=value)

        if record.get_state():
            print("Inserting command into db...")
            insert_route(conn, path, value, timestamp=datetime.now())

    elif path == '/start':
        print("Now recording commands...")
        # Clear any previous routes from the table
        cur = conn.cursor()
        cur.execute('delete from routes')
        conn.commit()
        record.set_state(True)

    elif path == '/stop':
        print("Stop recording selected. Current routes saved...")
        output_routes(conn)
        insert_route(conn, command="stop", val=0, timestamp=datetime.now())
        record.set_state(False)

    elif path == '/play':
        print("Play selected. Now repeating the saved route...")
        repeat_route(conn)

conn = init_db()
run_server(port=8000)
