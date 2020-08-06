from flask import Flask, request
import json
import requests
from pymysql import IntegrityError
import pokemon_data
import trainer_data
import type_data
import pokemonApi
import food_data

app = Flask(__name__, static_url_path='', static_folder='picture')


@app.route('/')
def root():
    file_path = 'pi.png'
    return app.send_static_file(file_path)


@app.route('/pokemons_pokemon/<name_pokemon>')
def get_owner_by_pokemon(name_pokemon):
    try:
        result = trainer_data.get_trainer_by_pokemon(name_pokemon)
        if not result:
            return json.dumps({"ERROR": "owner for pokemon not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/pokemons_owner/<name_trainer>')
def get_pokemon_by_owner(name_trainer):
    try:
        result = pokemon_data.get_pokemon_by_trainer(name_trainer)
        if not result:
            return json.dumps({"ERROR": "pokemon for owner not fount :("}), 404
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/pokemons_type/<type>')
def get_pokemons_by_type(type):
    try:
        result = type_data.get_pokemon_by_type(type)
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
    try:
        trainer_data.delete_pokemon_and_trainer_data(pokemon_trainer.get('trainer'), pokemon_trainer.get('pokemon'))
        return {"Status": "Succes, deleted pokemon and trainer"}, 201
    except Exception as error:
        code, message = error.args
        return {"Error": "This pokemon and trainer not exist"}, 409


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon_to_add = request.get_json()
    mandatory_params = ["id", "name", "height", "weight"]
    missing_params = [fields for fields in mandatory_params if not pokemon_to_add.get(fields)]
    if missing_params:
        return {"Error": f"fields {missing_params} are missing"}, 400
    list_types = pokemon_to_add.get("type")
    try:
        pokemon_data.add_pokemon(pokemon_to_add.get("id"), pokemon_to_add.get("name"), pokemon_to_add.get("height"), pokemon_to_add.get("weight"))
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pokemon already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    try:
        type_data.add_to_type(list_types)
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    try:
        type_data.add_to_pokemontype_list(pokemon_to_add.get("id"), list_types)
        return {"Status": "Succes, Added pokemon"}, 201
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/update_type/<name_pokemon>', methods=["PUT"])
def update_type(name_pokemon):
    pokemon = pokemonApi.find_pokemon(name_pokemon)
    try:
        list_type = type_data.get_types(name_pokemon)
        if not list_type:
            return json.dumps({"ERROR": "pokemon not fount :("}), 404
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    try:
        for type in pokemon.json()["types"]:
            if type['type']['name'] not in list_type:
                type_data.add_to_pokemontype(pokemon.json()["id"], type['type']['name'])
                pokemonApi.add_to_type_api(pokemon.json()["types"])
        return {"Status": "Succes, update pokemon"}, 201
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This type already exist"}, 409
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/evolve', methods=["PUT"])
def evolve():
    pokemon_to_evolve = request.get_json()
    try:
        result_id = trainer_data.get_id_by_pokemon_and_trainer(request.get_json()["name_pokemon"], request.get_json()["name_trainer"])
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    if not result_id:
        return {"Error": "This pair pokemon & trainer not exit"}, 404
    evolution = pokemonApi.find_evolution(pokemon_to_evolve.get("name_pokemon"))
    if not len(evolution):
        return {"ERROR": "pokemon can not evolve"}, 404
    chain_url = evolution[0]["species"]["url"]
    chain = requests.get(url=chain_url, verify=False)
    evolve = pokemonApi.find_evolve(evolution[0]["species"]["name"])
    try:
        result = pokemon_data.get_name_pokemon(pokemon_to_evolve["name_pokemon"])
        if result:
            try:
                result_id = trainer_data.get_id_by_pokemon_and_trainer(evolve.json()["name"], pokemon_to_evolve["name_trainer"])
            except Exception as e:
                return json.dumps({"ERROR": str(e)}), 500
            try:
                print(result_id)
                if not result_id:
                    pokemon_data.update_pokemon(evolve.json()["id"], evolution[0]["species"]["name"], pokemon_to_evolve["name_pokemon"],
                                                                    pokemon_to_evolve["name_trainer"])
                    return {"Status": "Succes, evolve pokemon"}, 201
                else:
                    return {"Error": "This pairs already exist"}, 409
            except Exception as e:
                return json.dumps({"ERROR": str(e)}), 500
        else:
            try:
                add_pokemon(evolve.json()["id"],evolution[0]["species"]["name"],
                            evolve.json()["height"],evolve.json()["weight"])
                type_data.add_to_type(evolve.json()["types"])
                type_data.add_to_pokemontype(evolve.json()["id"], evolve.json()["types"])
            except IntegrityError as error:
                code, message = error.args
                return {"Error": "This pokemon already exist"}, 409
    except IntegrityError as error:
        code, message = error.args
        return {"Error": "This pair pokemon & trainer not found"}, 404
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500


@app.route('/feed', methods=["DELETE"])
def feed_pokemon():
    pokemon_to_feed = request.get_json()
    try:
        result = trainer_data.get_id_by_pokemon_and_trainer(pokemon_to_feed.get("pokemon"), pokemon_to_feed.get("trainer"))
    except Exception as e:
        return json.dumps({"ERROR": str(e)}), 500
    if not result:
        return {"Error": "This pair pokemon & trainer not exit"}, 404
    list_types = type_data.get_types_feed(pokemon_to_feed.get("pokemon"))
    print(list_types)
    if not isinstance(list_types, list):
        list_types = [list_types]
    list_sensitive_food = food_data.get_sensitive_food(list_types)
    list_sensitive_food = [food['name_food'] for food in list_sensitive_food[0]]
    print(list_sensitive_food)
    if pokemon_to_feed.get("food") in list_sensitive_food:
        try:
            print(pokemon_to_feed.get("pokemon"), pokemon_to_feed.get("trainer"))
            trainer_data.delete_pokemon_and_trainer_data_food(pokemon_to_feed.get("pokemon"),
                                                         pokemon_to_feed.get("trainer"))
            return {"Status": 'Oops Pokemon {} is dead you have fed {} and it is {} sensitive'.format(
                pokemon_to_feed.get("pokemon"),
                pokemon_to_feed.get("food"),
                pokemon_to_feed.get("food"))}, 201
        except Exception as error:
            code, message = error.args
            return {"Error": "This pokemon and trainer not exist"}, 409
    else:
        return {"Status": 'Bravo you fed your Pokemon {} and now he is full'.format(
            pokemon_to_feed.get("pokemon"))}, 201


port_number = 3000
if __name__ == '__main__':
    app.run(port=port_number)
