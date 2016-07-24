import sys
sys.path.append("..")
from flask import Flask, request, g, render_template, url_for, redirect, session
from db_conn import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@db_wrapper
def search(c, artist):
	# c.execute("""SELECT name, gen, uri
	# 			 FROM kanye_degree
	# 			 WHERE name LIKE ?
	# 	      	 """, ('%'+artist+'%',))
	c.execute("""SELECT name, gen, uri
				 FROM kanye_degree
				 WHERE name LIKE ?
		      	 """, (artist,))
	return c.fetchone()

@db_wrapper
def search_by_uri(c, uri):
	c.execute("""SELECT name, gen, uri
				 FROM kanye_degree
				 WHERE uri=?""", (uri, ))
	return c.fetchone()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/artist", methods=['POST'])
def degree():
	artist = request.form['artist']
	name, gen, uri = search(artist)
	session['name'] = name
	session['gen'] = gen
	# return render_template('index.html', name=name.upper(), gen=gen)
	return redirect(url_for('get_page', uri=uri))

@app.route('/artist/<string:uri>')
def get_page(uri):
	name, gen, uri = search_by_uri(uri)
	return render_template('index.html', name=name.upper(), gen=gen)


if __name__ == "__main__":
	app.run(debug=True)
