import sqlite3
from datetime import datetime
import time


class Record:
    def __init__(self):
        self.state = False

    def set_state(self, val):
        self.state = val

    def get_state(self):
        return self.state


def init_db():
    # Store route in database file
    conn = sqlite3.connect('route.db')

    # Initialize data table
    conn.execute('''CREATE TABLE IF NOT EXISTS routes
                        (command text, value int, timestamp date)''')

    # Clear any previous data
    cur = conn.cursor()
    cur.execute('delete from routes')
    conn.commit()

    return conn


def insert_route(conn, command, val, timestamp):
    cur = conn.cursor()
    cur.execute("insert into routes (command, value, timestamp) values (?, ?, ?)", (command, val, timestamp))
    conn.commit()


def output_routes(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM routes")

    rows = cur.fetchall()
    for row in rows:
        print(row)


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


# Forward the message along to the hardware side. For now just print out a message to console
def send_to_hardware(command, val):

    if command == 'fb':
        print("Forward/Backward Slider: ", val)
    elif command == 'lr':
        print("Left/Right Slider: ", val)
    else:
        print("Invalid Command: ", command)
