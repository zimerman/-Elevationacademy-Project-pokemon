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


@app.route('/pokemons_owner/<name_trainer>')
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
    ON pokemon.id = pokemontype.id_pokemon AND pokemontype.name_type = '{}'""".format(
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


@app.route('/delete_pokemon_trainer', methods=['DELETE'])
def delete_pokemon_and_trainer():
    pokemon_trainer = request.get_json()
    mandatory_params = ["pokemon", "trainer"]
    missing_params = [params for params in mandatory_params if not pokemon_trainer.get(params)]
    if missing_params:
        return {"Error": f"params {missing_params} are missing"}, 400
    query = "DELETE FROM ownedby WHERE name_trainer = '{}' AND id_pokemon = (SELECT id FROM pokemon WHERE name = '{}')".format(
        pokemon_trainer.get('pokemon'),
        pokemon_trainer.get('trainer')
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return {"Status": "Succes, deleted pokemon and trainer"}, 201
    except Exception as error:
        code, meesage = error.args
        return {"Error": "This pokemon and trainer not exist"}, 409
    # except Exception as e:
    #     return json.dumps({"ERROR": str(e)}), 500


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon_to_add = request.get_json()
    mandatory_fields = ["id", "name", "height", "weight"]
    missing_params = [fields for fields in mandatory_fields if not pokemon_to_add.get(fields)]
    if missing_params:
        return {"Error": f"fields {missing_params} are missing"}, 400
    list_types = pokemon_to_add.get("type")
    query = "INSERT into pokemon values ({},'{}',{},{})".format(
        pokemon_to_add.get("id"),
        pokemon_to_add.get("name"),
        pokemon_to_add.get("height"),
        pokemon_to_add.get("weight")
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return {"Status": "Succes, Added pokemon"}, 201
    except Exception as error:
        code, meesage = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    for type in list_types:
        query2 = "INSERT into pokemontype values({}, '{})".format(
            pokemon_to_add.get("id"),
            type
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return {"Status": "Succes, Added pokemon"}, 201
        except Exception as error:
            code, meesage = error.args
            return {"Error": "This pokemon and trainer not exist"}, 409
        except Exception as e:
            return json.dumps({"ERROR": str(e)}), 500


port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
