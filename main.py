import re
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_cafes():
    conn = sqlite3.connect("cafes.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM cafe")
    return res.fetchall()


@app.route("/")
def home():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)


if __name__ == "__main__":
    app.run()
