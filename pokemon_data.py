import pymysql
from conect import connection


def get_pokemon_by_trainer(name_trainer):
    query = """SELECT name from pokemon
                WHERE id in
                (SELECT ownedby.id_pokemon
                FROM trainers JOIN ownedby
                ON ownedby.name_trainer = trainers.name AND trainers.name = '{}')""".format(name_trainer)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def add_pokemon(id, name, height, weight):
    query = "INSERT into pokemon values ({},'{}',{},{})".format(
        id,
        name,
        height,
        weight)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def get_name_pokemon(name):
    query = """SELECT name
                   FROM pokemon
                   WHERE name = '{}'""".format(name)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchone()
    return result


def update_pokemon(id, name, name_pokemon, name_trainer):
    query = """UPDATE ownedby
               SET id_pokemon = {}, name_pokemon = '{}'
               WHERE name_pokemon = '{}' AND name_trainer = '{}'""".format(
        id,
        name,
        name_pokemon,
        name_trainer)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

