from db_conn import *


@db_wrapper
def a(c):
    c.execute("SELECT artist FROM ft_artists WHERE artist='Eminem'")
    a = c.fetchall()
    print a

a()