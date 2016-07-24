import sqlite3
import os

db_dir = os.path.dirname(__file__)

def open_conn():
    """Opens database connection."""
    conn = sqlite3.connect(db_dir+"/release_info.db")
    c = conn.cursor()

    return conn, c

def close_conn(conn):
    """Closes database connection."""
    conn.commit()
    conn.close()

def db_wrapper(function):
    """
    Wraps a function in the database connection.

    Allows some functionality to be added and database doesn't have to opened
    and closed manually each time - instead we can just add a decorator for
    the function using the database.
    """
    def wrapper(*args, **kwargs):
        conn, c = open_conn()
        f = function(c, *args, **kwargs)
        close_conn(conn)
        return f

    return wrapper
