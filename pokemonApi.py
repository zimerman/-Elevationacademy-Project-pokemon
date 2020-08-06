from conect import connection
import requests


def add_to_type_api(list_types):
    for type in list_types:
        query = "INSERT into type values('{}')".format(type["type"]["name"])
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()


def find_evolve(name):
    evolve = requests.get(url='https://pokeapi.co/api/v2/pokemon/{}'.format(name), verify=False)
    return evolve


def find_evolution(name):
    pokemon = requests.get(url='https://pokeapi.co/api/v2/pokemon/{}'.format(name), verify=False)
    species = requests.get(url=pokemon.json()["species"]["url"], verify=False)
    evolution = requests.get(url=species.json()["evolution_chain"]["url"], verify=False).json()["chain"]["evolves_to"]
    return evolution


def find_pokemon(name_pokemon):
    pokemon = requests.get(url='https://pokeapi.co/api/v2/pokemon/{}'.format(name_pokemon), verify=False)
    return pokemon