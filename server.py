import http.server
from record_route import *
from datetime import datetime


# State variable to keep track if the route requests should be recorded for playback
record = Record()


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        handle_request(post_data)


def run_server(port, server_class=http.server.HTTPServer, handler_class=ToyHandler):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Serving PORT: ", port)
    httpd.serve_forever()


# Parse the POST and fire off a function based on the command
def handle_request(post_data):

    # If it has an equals sign its a slider request for forward/back/left/right
    if len(post_data.split('=')) > 1:
        command, val = post_data.split('=')
        send_to_hardware(command, val)

        # If we're in record mode store the command in the db
        if record.get_state():
            print("Inserting route into db...")
            insert_route(conn, command, val, datetime.now())

    # Otherwise its a button request to start/stop/play a recorded route
    else:
        if post_data == 'start':
            print("Start recording selected...")
            # Clear any previous routes from the table
            cur = conn.cursor()
            cur.execute('delete from routes')
            conn.commit()
            record.set_state(True)

        elif post_data == 'stop':
            print("Stop recording selected. Current routes saved...")
            output_routes(conn)
            insert_route(conn, command="stop", val=0, timestamp=datetime.now())
            record.set_state(False)

        elif post_data == 'play':
            print("Play selected. Now repeating the saved route...")
            repeat_route(conn)


conn = init_db()
run_server(port=8000)
