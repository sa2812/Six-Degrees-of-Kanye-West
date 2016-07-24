import sys
sys.path.append("..")
from flask import Flask, request, g, render_template
from db_conn import *

app = Flask(__name__)

@db_wrapper
def search(c, artist):
	c.execute("""SELECT uri
				 FROM kanye_degree
				 WHERE name LIKE ?
		      	 """, ('%'+artist+'%',))
	return c.fetchone()

@app.route("/")
def index():
	a = search('jay z')
	return render_template('index.html', uri=a)

@app.route("/artist/<artist_uri>")
def degree(artist_uri):
	return render_template('index.html', uri=artist_uri)

if __name__ == "__main__":
	app.run(debug=True)
