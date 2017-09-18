import sqlite3
from datetime import datetime
import time
import math


class Record:
    def __init__(self):
        self.state = False

    def set_state(self, val):
        self.state = val

    def get_state(self):
        return self.state


# Store route in database file
def init_db():
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




