from flask import Flask, Response, request
import pymysql
import json

import requests
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
    query = "SELECT id FROM pokemon JOIN pokemontype ON pokemon.id = pokemontype.id_pokemon AND pokemontype.name_type = '{}'".format(
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
    query = """DELETE FROM ownedby 
            WHERE name_trainer = '{}' AND id_pokemon = 
            (SELECT id FROM pokemon WHERE name = '{}')""".format(
        pokemon_trainer.get('trainer'),
        pokemon_trainer.get('pokemon')
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return {"Status": "Succes, deleted pokemon and trainer"}, 201
    except Exception as error:
        code, message = error.args
        return {"Error": "This pokemon and trainer not exist"}, 409


def add_to_pokemontype(id_, list_types):
    try:
        for type in list_types:
            query2 = "INSERT into pokemontype values({}, '{}')".format(
                id_,
                type
            )
            with connection.cursor() as cursor:
                cursor.execute(query2)
                connection.commit()
        return {"Status": "Succes, Added pokemon"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


def add_to_type(list_types):
    try:
        for type in list_types:
            query = "INSERT into type values('{}')".format(type)
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        return {"Status": "Succes, Added type"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This type already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


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
            add_to_type(list_types)
            add_to_pokemontype(pokemon_to_add.get("id"), list_types)
            return {"Status": "Succes, Added pokemon"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
         return json.dumps({"ERROR": str(e)}), 500


def get_id_by_name(name_pokemon):
    query = "SELECT id FROM pokemon WHERE name = '{}'".format(name_pokemon)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return json.dumps({"ERROR": "pokemon not fount :("}), 404
        return json.dumps(result["id"])
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


def add_to_type_api(list_types):
    try:
        for type in list_types:
            query = "INSERT into type values('{}')".format(type["type"]["name"])
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        return {"Status": "Succes, Added type"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This type already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


def get_types(name_pokemon):
    query = "SELECT name_type FROM pokemontype JOIN pokemon ON pokemontype.id_pokemon = pokemon.id AND name = '{}'".format(name_pokemon)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return json.dumps({"ERROR": "pokemon not fount :("}), 404
        return json.dumps(result["name_type"])
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/update_type/<name_pokemon>', methods=["PUT"])
def update_type(name_pokemon):
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(name_pokemon)
    pokemon = requests.get(url=pokemon_url, verify=False)
    try:
        for type in pokemon.json()["types"]:
            if type['type']['name'] not in get_types(name_pokemon):
                query = "INSERT into pokemontype values ({},'{}')".format(
                    pokemon.json()["id"], type['type']['name'])
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                add_to_type_api(pokemon.json()["types"])
        return {"Status": "Succes, Added pokemon"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


def get_id_by_pokemon_and_trainer(name_pokemon,name_trainer):
    query = """SELECT id
               FROM
               WHERE name = '{}' AND name_trainer = '{}'""".format(
        name_pokemon,
        name_trainer
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return json.dumps({"ERROR": "pokemon and trainer not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/Evolve', methods=["PUT"])
def evolve():
    pokemon_to_evolve = request.get_json()
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format("ivysaur")
    pokemon = requests.get(url=pokemon_url, verify=False)
    species_url = pokemon.json()["species"]["url"]
    species = requests.get(url=species_url, verify=False)
    evolution_url = species.json()["evolution_chain"]["url"]
    evolution = requests.get(url=evolution_url, verify=False)
    chain_url = evolution.json()["chain"]["evolves_to"][0]["species"]["url"]
    chain = requests.get(url=chain_url, verify=False)
    evolve_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(pokemon_to_evolve["name_pokemon"])
    evolve = requests.get(url=evolve_url, verify=False)
    query = """SELECT name
               FROM pokemon
               WHERE name = '{}'""".format(
        pokemon_to_evolve["name_pokemon"]
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result:
            query = """UPDATE ownedby
                       SET id_pokemon = {}, name_pokemon = '{}'
                       WHERE name_pokemon = '{}' AND name_trainer = '{}'""".format(
                evolve.json()["id"],
                evolution.json()["chain"]["evolves_to"][0]["species"]["name"],
                pokemon_to_evolve["name_pokemon"],
                pokemon_to_evolve["name_trainer"])
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        else:
            query = """INSERT into pokemon values ({},'{}',{},{})""".format(
                evolve.json()["id"],
                evolution.json()["chain"]["evolves_to"][0]["species"]["name"],
                evolve.json()["height"],
                evolve.json()["weight"]
            )
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500




port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
