import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def get_by_title(title):
    db_connect = DbConnect("netflix.db")
    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title = '{title}'
            """
    result = db_connect.cur.execute(query)
    result = result.fetchone()
    dict_result = {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }
    return dict_result


def get_by_between_years(year1, year2):
    db_connect = DbConnect("netflix.db")
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year1} AND {year2}
            ORDER BY release_year
            LIMIT 100
            """
    result = db_connect.cur.execute(query)
    results = result.fetchall()
    list_result = []
    for result in results:
        list_result.append(
            {
                "title": result[0],
                "release_year": result[1]
            })
    return list_result


def get_by_rating(group_key):
    groups = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    db_connect = DbConnect("netflix.db")
    try:
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating in ({groups[group_key]})
                ORDER BY rating
                """
    except KeyError:
        list_result = [{"ERROR": "Нет такой возрастной категории"}]
    else:
        result = db_connect.cur.execute(query)
        results = result.fetchall()
        list_result = []
        for result in results:
            list_result.append(
                {
                    "title": result[0],
                    "rating": result[1],
                    "description": result[2]
                })
    return list_result


def get_by_genre(genre):
    db_connect = DbConnect("netflix.db")
    query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC
                LIMIT 10
                """
    result = db_connect.cur.execute(query)
    results = result.fetchall()
    list_result = []
    for result in results:
        list_result.append(
            {
                "title": result[0],
                "description": result[1]
            })
    return list_result


def cast_partners(actor1, actor2):
    db_connect = DbConnect("netflix.db")
    query = f"""
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE '%{actor1}%'
                    AND 
                    "cast" LIKE '%{actor2}%'
                    """
    result = db_connect.cur.execute(query)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list


def get_movie_by_tyg(type_movie, year, genre):
    db_connect = DbConnect("netflix.db")
    query = f"""
                SELECT type, release_year, listed_in
                FROM netflix
                WHERE type = '{type_movie}' AND
                release_year = '{year}' AND
                listed_in = '{genre}'
                ORDER BY release_year
                """
    result = db_connect.cur.execute(query)
    results = result.fetchall()
    list_result = []
    for result in results:
        list_result.append(
            {
                "type": result[0],
                "release_year": result[1],
                "genre": result[2]
            })
    return list_result
