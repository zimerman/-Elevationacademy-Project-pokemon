from conect import connection
import requests

def add_to_type_api(list_types):
    for type in list_types:
        query = "INSERT into type values('{}')".format(type["type"]["name"])
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()


def find_evolution(name):
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(name)
    pokemon = requests.get(url=pokemon_url, verify=False)
    species_url = pokemon.json()["species"]["url"]
    species = requests.get(url=species_url, verify=False)
    evolution_url = species.json()["evolution_chain"]["url"]
    evolution = requests.get(url=evolution_url, verify=False).json()["chain"]["evolves_to"]
    return evolution


def find_evolve(name):
    evolve_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(name)
    evolve = requests.get(url=evolve_url, verify=False)
    return evolve

