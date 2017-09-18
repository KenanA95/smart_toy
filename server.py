import http.server
from record_route import *
from datetime import datetime
from test_robot import Robot
import json


# State variable to keep track if the route requests should be recorded for playback
record = Record()

# Testing class to forward commands to
robot = Robot()


class ToyHandler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_response(200)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        length = int(self.headers['Content-Length'])
        value = json.loads(self.rfile.read(length).decode('utf-8'))
        handle_request(self.path, int(value['value']))
        self.end_headers()


def run_server(port):

    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, ToyHandler)
    print("Serving PORT: ", port)
    httpd.serve_forever()


def handle_request(path, value):
    path = path.strip()

    if path == '/forwardBackward' or path == '/leftRight':
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


# Parse and forward the command from the UI to the robot
# Value from the front-end slider comes in the range 0-100 where 1-49 is backwards 50 is neutral
# and 51-100 is forward. This value is mapped to the robot in the range of 0-100
def send_to_hardware(command, val):

    if command == '/forwardBackward':
        if 0 < val < 50:
            val = scale_value(val, current_range=49)
            robot.go_backward(val)
        elif val == 50:
            robot.stop()
        elif val > 50:
            val = scale_value(val, current_range=99)
            robot.go_forward(val)

    elif command == '/leftRight':
        if 0 <= val < 50:
            robot.turn_left()
        elif val == 50:
            robot.straight()
        elif val >= 50:
            robot.turn_right()


# Map to 1-100 range
def scale_value(value, current_range):
    new_range = 99
    scaled_value = (((value-1) * new_range) / current_range) + 1
    return math.ceil(scaled_value)


def repeat_route(conn):
    # Pull all records
    cur = conn.cursor()
    cur.execute("SELECT * FROM routes")
    rows = cur.fetchall()

    for index, row in enumerate(rows):
        if row[0] == 'stop':
            print("Completed the recorded route...")
            return

        command, val = row[0], row[1]

        # Figure out how long to wait until sending off the next command
        start_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        stop_time = datetime.strptime(rows[index + 1][2], '%Y-%m-%d %H:%M:%S.%f')
        duration = (stop_time - start_time).total_seconds()

        send_to_hardware(command, val)
        time.sleep(duration)


conn = init_db()
run_server(port=8000)
