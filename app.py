from flask import Flask, jsonify, render_template
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/movie/<title>")
def get_by_title_page(title):
    result = get_by_title(title)
    return jsonify(result)


@app.route("/movie/<year1>/to/<year2>")
def get_by_between_years_page(year1, year2):
    result = get_by_between_years(year1, year2)
    return jsonify(result)


@app.route("/rating/<group_rating>")
def get_by_rating_page(group_rating):
    result = get_by_rating(group_rating)
    return jsonify(result)


@app.route("/genre/<genre>")
def get_by_genre_page(genre):
    genre = genre.lower()
    result = get_by_genre(genre)
    return jsonify(result)


@app.route("/cast-partners/<actor1>/and/<actor2>")
def cast_partners_page(actor1, actor2):
    result = cast_partners(actor1, actor2)
    return jsonify(result)


@app.route("/movie-by-tyg/<movie_type>/<year>/<genre>")
def get_movie_by_tyg_page(movie_type, year, genre):
    result = get_movie_by_tyg(movie_type, year, genre)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
