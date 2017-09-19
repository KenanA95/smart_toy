import http.server
from record_route import *
from datetime import datetime
from test_robot import Robot
import json
import numpy as np
from scipy.interpolate import interp1d


# State variable to keep track if the route requests should be recorded for playback
record = Record()

# Testing class to forward commands to
robot = Robot()


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        value = 0

        # Parse the value from the sliders
        if self.path == '/forwardBackward' or self.path == '/leftRight':
            length = int(self.headers['Content-Length'])
            value = json.loads(self.rfile.read(length).decode('utf-8'))
            value = int(value['value'])

        handle_request(self.path, value)


def handle_request(path, value):

    if path == '/forwardBackward' or path == '/leftRight':
        send_to_hardware(command=path, val=value)

        if record.get_state():
            # Insert the command/timestamp
            insert_route(conn, path, value, timestamp=datetime.now())

    elif path == '/start':
        # Clear any previous routes from the table
        cur = conn.cursor()
        cur.execute('delete from routes')
        conn.commit()
        record.set_state(True)

    elif path == '/stop':
        # output_routes(conn)
        insert_route(conn, command="stop", val=0, timestamp=datetime.now())
        record.set_state(False)

    elif path == '/play':
        print("Play selected. Now repeating the saved route...")
        repeat_route(conn)


def run_server(port):

    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, ToyHandler)
    print("Serving PORT: ", port)
    httpd.serve_forever()


# Parse and forward the command from the UI to the robot
# Value from the front-end slider comes in the range 0-100 where 0-49 is backwards 50 is neutral
# and 51-100 is forward. This value is mapped to the robot in the range of 0-100
def send_to_hardware(command, val):

    if command == '/forwardBackward':
        if 0 <= val < 50:
            val = scale_backward_value(val)
            robot.go_backward(val)
        elif val == 50:
            robot.stop()
        elif val > 50:
            val = scale_forward_value(val)
            robot.go_forward(val)

    elif command == '/leftRight':
        if 0 <= val < 50:
            robot.turn_left()
        elif val == 50:
            robot.straight()
        elif val >= 50:
            robot.turn_right()


# Map from 51-100 to 1-100 range
def scale_forward_value(value):
    f = interp1d([51, 100], [1, 100])
    return int(np.round(f(value)))


# Map from 0-49 to 1-100 range where 0 is the fastest and 49 is the slowest
def scale_backward_value(value):
    f = interp1d([0, 49], [100, 1])
    return int(np.round(f(value)))


def repeat_route(conn):
    # Pull all records from the file
    cur = conn.cursor()
    cur.execute("SELECT * FROM routes")
    rows = cur.fetchall()

    for index, row in enumerate(rows):
        # Get the command sent by the user and its associated value
        command, val = row[0], row[1]

        # Reached the last command
        if command == 'stop':
            print("Completed the recorded route...")
            return

        else:
            # Figure out how long to wait until sending off the next command
            start_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
            stop_time = datetime.strptime(rows[index + 1][2], '%Y-%m-%d %H:%M:%S.%f')
            duration = (stop_time - start_time).total_seconds()
            send_to_hardware(command, val)
            # Wait the original amount of time as the command before a different command was sent
            time.sleep(duration)


conn = init_db()
run_server(port=8000)
