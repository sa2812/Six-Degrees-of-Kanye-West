import sys
sys.path.append("..")
from flask import Flask, request, g, render_template, url_for, redirect, session, flash
from web_db_conn import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@db_wrapper
def search(c, artist):
	c.execute("""SELECT name, gen, id
				 FROM kanye_degree
				 WHERE name LIKE ?""", ('%'+artist+'%',))
	return c.fetchone()

@db_wrapper
def search_by_id(c, _id):
	c.execute("""SELECT name, gen, id
				 FROM kanye_degree
				 WHERE id=?""", (_id, ))
	return c.fetchone()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/artist", methods=['POST'])
def degree():
	artist = request.form['artist']
	try:
		name, gen, _id = search(artist)
	except TypeError:
		flash("Artist not found")
		return redirect(url_for('index'))
	session['name'] = name
	session['gen'] = gen
	return redirect(url_for('get_page', _id=_id))

@app.route('/artist/<string:_id>', methods=['GET', 'POST'])
def get_page(_id):
	if request.method == 'POST':
		name = session['name']
		gen = session['gen']
		try:
			return render_template('index.html', name=name.upper(), gen=gen)
		except NameError:
			flash("Artist not found")
			return redirect(url_for('index'))
	name, gen, _id = search_by_id(_id)
	try:
		return render_template('index.html', name=name.upper(), gen=gen)
	except NameError:
		flash("Artist not found")
		return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(host="0.0.0.0")
