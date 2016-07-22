from flask import Flask, request, g, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello world!"

if __name__ == "__main__":
	app.run()