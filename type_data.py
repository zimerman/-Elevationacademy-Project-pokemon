import pymysql
import json
from pymysql import IntegrityError

from conect import connection


def get_pokemon_by_type(type):
    query = """SELECT id
               FROM pokemon JOIN pokemontype
               ON pokemon.id = pokemontype.id_pokemon AND pokemontype.name_type = '{}'""".format(
        type
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def add_to_type(list_types):
    for type in list_types:
        query = "INSERT into type values('{}')".format(type)
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()


def get_types(name_pokemon):
    query = "SELECT name_type FROM pokemontype JOIN pokemon ON pokemontype.id_pokemon = pokemon.id AND name = '{}'".format(name_pokemon)
    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchone()
    if not result:
        return result
    return json.dumps(result.get("name_type"))


def add_to_pokemontype(id_, type):
    query2 = "INSERT into pokemontype values({}, '{}')".format(
        id_, type)
    with connection.cursor() as cursor:
        cursor.execute(query2)
        connection.commit()