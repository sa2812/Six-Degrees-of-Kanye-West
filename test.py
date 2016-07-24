from db_conn import *

@db_wrapper
def search(c, artist):
	c.execute("""SELECT uri
				 FROM kanye_degree
				 WHERE name LIKE ?
		      	 """, ('%'+artist+'%',))
	return c.fetchone()

print search('jay z')