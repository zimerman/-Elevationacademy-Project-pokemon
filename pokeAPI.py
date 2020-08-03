from flask import Flask, Response, request
import pymysql
import json
from pymysql import IntegrityError

app = Flask(__name__)

connection = pymysql.connect(
    host="localhost",
    user="admin",
    password="",
    db="sql_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")


@app.route('/pokemons_pokemon/<name_pokemon>')
def get_owner_by_pokemon(name_pokemon):

    query = """SELECT name from trainers
             WHERE name in
             (SELECT ownedby.name_trainer
              FROM pokemon JOIN ownedby 
              ON pokemon.id = ownedby.id_pokemon AND pokemon.name = '{}')""".format(name_pokemon)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        if not result:
            return json.dumps({"ERROR": "owner for pokemon not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/pokemons_owner/<name_owner>')
def get_pokemon_by_owner(name_trainer):

    query = """SELECT name from pokemon
            WHERE id in
            (SELECT ownedby.id_pokemon 
            FROM trainers JOIN ownedby 
            ON ownedby.name_trainer = trainers.name AND trainers.name = '{}')""".format(name_trainer)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        if not result:
            return json.dumps({"ERROR": "pokemon for owner not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/pokemons_type/<type>')
def get_pokemons_by_type(type):
    query = """"SELECT id 
    FROM pokemon JOIN pokemontype
    ON pokemon.id = pokemontype.id_pokemon AND name_type = '{}'""".format(
        type
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return json.dumps({"ERROR": "pokemon for type not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
