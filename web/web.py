import sys
sys.path.append("..")
from flask import Flask, request, g, render_template, url_for, redirect, session, flash
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
				 ORDER BY length(name)
		      	 """, ('%'+artist+'%',))
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
	try:
		name, gen, uri = search(artist)
	except TypeError:
		flash("Artist not found")
		return redirect(url_for('index'))
	session['name'] = name
	session['gen'] = gen
	return redirect(url_for('get_page', uri=uri))

@app.route('/artist/<string:uri>', methods=['GET', 'POST'])
def get_page(uri):
	if request.method == 'POST':
		name = session['name']
		gen = session['gen']
		try:
			return render_template('index.html', name=name.upper(), gen=gen)
		except NameError:
			flash("Artist not found")
			return redirect(url_for('index'))
	name, gen, uri = search_by_uri(uri)
	try:
		return render_template('index.html', name=name.upper(), gen=gen)
	except NameError:
		flash("Artist not found")
		return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(host="0.0.0.0")
