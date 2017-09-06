import http.server
from record_route import *
from datetime import datetime


# State variable to keep track if the route requests should be recorded for playback
record = Record()


#
class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        handle_request(post_data)


# TODO: Refactor
def handle_request(post_data):

    # Otherwise its a button request to record a route
    if len(post_data.split('=')) == 1:
        if post_data == 'start':
            print("Start recording selected...")
            record.set_state(True)
            # Clear the current table
            cur = conn.cursor()
            cur.execute('delete from routes')
            conn.commit()

        elif post_data == 'stop':
            record.set_state(False)
            print("Stop recording selected. Current routes saved...")
            output_routes(conn)
            # repeat_route(conn)

    # If it has an equals sign its a slider request
    else:
        command, val = post_data.split('=')
        send_to_hardware(command, val)

        if record.get_state():
            print("Inserting route...")
            insert_route(conn, command, val, datetime.now())


# Forward the message along to the hardware side. For now just print out a message to console
def send_to_hardware(command, val):

    if command == 'fb':
        print("Forward/Backward Slider:  ", val)
    elif command == 'lr':
        print("Left/Right Slider ", val)
    else:
        print("Invalid Command: ", command)


def run_server(port, server_class=http.server.HTTPServer, handler_class=ToyHandler):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Serving PORT: ", port)
    httpd.serve_forever()


conn = init_db()
run_server(port=8000)
