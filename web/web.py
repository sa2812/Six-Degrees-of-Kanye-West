from flask import Flask, request, g, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/<artist_uri>")
def degree(artist_uri):
	return render_template('index.html', uri=artist_uri)

if __name__ == "__main__":
	app.run()
