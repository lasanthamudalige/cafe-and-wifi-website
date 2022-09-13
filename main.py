from flask import Flask, render_template, redirect
from flask import request
import sqlite3

app = Flask(__name__)


# Load all the cafes for cafes.db


def get_cafes():
    conn = sqlite3.connect("cafes.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM cafe")
    return res.fetchall()


def add_new_cafe(name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats=0, coffee_price=0):
    conn = sqlite3.connect("cafes.db")
    cur = conn.cursor()
    # Get all cafes
    res = cur.execute("SELECT * FROM cafe").fetchall()
    # Get last id from last cafe
    last_id = res[-1][0]
    new_id = last_id + 1

    # Add cafe to cafe.db
    cur.execute(
        f"INSERT INTO cafe VALUES({new_id}, '{name}', '{map_url}', '{img_url}', '{location}', {has_sockets}, {has_toilet}, {has_wifi}, {can_take_calls}, '{seats}', '{coffee_price}')")
    conn.commit()
    conn.close()


@app.route("/")
def home():
    cafes = get_cafes()
    # Get index of last cafe and add 1 to it
    total_cafes = (cafes[-1][0]) + 1
    return render_template("index.html", cafes=cafes, total_cafes=total_cafes)


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":

        cafe_name = request.form.get("name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("img_url")
        location = request.form.get("location")
        seats = request.form.get("seats")
        coffee_price = request.form.get("coffee_price")
        has_sockets = request.form.get("has_sockets")
        has_toilet = request.form.get("has_toilet")
        has_wifi = request.form.get("has_wifi")
        can_take_calls = request.form.get("can_take_calls")

        # If below checkboxes checked
        if has_sockets == "on":
            has_sockets = 1
        else:
            has_sockets = 0

        if has_toilet == "on":
            has_toilet = 1
        else:
            has_toilet = 0

        if has_wifi == "on":
            has_wifi = 1
        else:
            has_wifi = 0

        if can_take_calls == "on":
            can_take_calls = 1
        else:
            can_take_calls = 0

        add_new_cafe(cafe_name, map_url, img_url, location,
                     has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)

        return redirect("/")

    return render_template("add_cafe.html")


if __name__ == "__main__":
    app.run()
