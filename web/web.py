import sys
sys.path.append("..")
from flask import Flask, request, g, render_template, url_for, redirect, session, flash
from web_db_conn import *
import spotipy
import json
import itertools
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

sp = spotipy.Spotify()
kanye_id = "5K4W6rqBFWDnAN6FQUkS6x"

specials = {'kimkardashian' 		 : {'type': 'youtube',
							   			'link_id': 'BBAtAM7vtgc',
							   			'nickname':'Kim K',
							  			'get_path': False},
			'06HL4z0CvFAxyc27GXpf02' : {'type': 'youtube',
										'link_id': 'p7FCgw_GlWc',
										'nickname': u'\U0001F40D',
										'get_path': True}}

@db_wrapper
def search(c, artist):
	c.execute("""SELECT name, gen, id
				 FROM kanye_degree
				 WHERE name LIKE ?
				 ORDER BY length(name) ASC""", ('%'+artist+'%',))
	return c.fetchone()

@db_wrapper
def search_artist_name(c, name):
	c.execute("""SELECT name
				 FROM kanye_degree
				 WHERE name LIKE ?
				 ORDER BY popularity DESC, gen ASC
				 LIMIT 5""", ('%'+name+'%',))
	return c.fetchall()

@db_wrapper
def select_random(c):
	loop = True
	while loop:
		c.execute("""SELECT name, gen, id
					 FROM kanye_degree
					 ORDER BY RANDOM()
					 LIMIT 1""")
		name, gen, _id = c.fetchone()
		if _id != kanye_id:
			return name, gen, _id


@db_wrapper
def search_by_id(c, _id):
	c.execute("""SELECT name, gen, id
				 FROM kanye_degree
				 WHERE id=?""", (_id, ))
	return c.fetchone()

@db_wrapper
def get_connection(c, _id):
	c.execute("""SELECT ancestor, track, track_name
				 FROM kanye_degree
				 WHERE id=?""", [_id])
	return c.fetchone()

@db_wrapper
def get_name_from_id(c, _id):
	c.execute("""SELECT name
				 FROM kanye_degree
				 WHERE id=?""", [_id])
	return c.fetchone()

def track_handler(track_id):
	name = get_track(track)[0]
	if name:
		return name
	else:
		return sp.track(track)['name']

def get_path(_id, path=None, track_ids=None, track_names=None):
	if not path:
		path = [_id]
		track_ids = []
		track_names = []
		snippets = []
	ancestor, track_id, track_name = get_connection(_id)
	ancestor_id = ancestor[15:]
	path.append(ancestor_id)
	track_ids.append(track_id)
	if track_name:
		track_names.append(track_name)
	else:
		track_names.append(sp.track(track_id)['name'])
	while ancestor_id != kanye_id:
		return get_path(ancestor_id, path, track_ids, track_names)
	path = [get_name_from_id(i)[0] for i in path]
	return path, zip(track_ids, track_names)

def render(name, gen, result, _id, _flash=None):
	try:
		if _flash:
			for i in _flash:
				flash(*i)
		return render_template('result.html', name=name,
							   gen=gen, result=result, _id=_id)
	except NameError:
		flash("Artist not found", "error")
		return redirect(url_for('index'))

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

@app.route('/<string:_id>', methods=['GET', 'POST'])
def get_page(_id):
	try:
		special = specials[_id]
		_flash = []
		# flash(special['type'], 'linktype')
		# flash(special['link_id'], 'link-id')
		_flash.append((special['nickname'], 'nickname'))
		_flash.append((special['link_id'], special['type']))
		if special['get_path']:
			result = [x for x in itertools.chain.from_iterable(itertools.izip_longest(*get_path(_id))) if x]
		else:
			result = []
		name, gen, _id = search_by_id(_id)
		return render(name, gen, result, _id, _flash)
	except KeyError:
		pass
	result = [x for x in itertools.chain.from_iterable(itertools.izip_longest(*get_path(_id))) if x]
	if request.method == 'POST':
		name = session['name']
		gen = session['gen']
		return render(name, gen, result, _id)
	else:
		name, gen, _id = search_by_id(_id)
		return render(name, gen, result, _id)

@app.route("/random")
def random():
	session['name'], session['gen'], _id = select_random()
	return redirect(url_for('get_page', _id=_id))

@app.route("/autocomplete", methods=['GET'])
def autocomplete():
	name = request.args.get('q')
	return json.dumps([ii[0] for ii in search_artist_name(name)])

@app.route("/about")
def about():
	return render_template('about.html')


if __name__ == "__main__":
	app.run(host="0.0.0.0")
