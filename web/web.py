from flask import Flask, request, g, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')


if __name__ == "__main__":
	app.run()
