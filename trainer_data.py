from conect import connection


def get_trainer_by_pokemon(name_pokemon):
    query = """SELECT name from trainers
                 WHERE name in
                 (SELECT ownedby.name_trainer
                  FROM pokemon JOIN ownedby
                  ON pokemon.id = ownedby.id_pokemon AND pokemon.name = '{}')""".format(name_pokemon)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def delete_pokemon_and_trainer_data(trainer, pokemon):
    query = """DELETE FROM ownedby
                WHERE name_trainer = '{}' AND id_pokemon =
                (SELECT id FROM pokemon WHERE name = '{}')""".format(
            trainer,
            pokemon
        )
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def get_id_by_pokemon_and_trainer(pokemon, trainer):
    query = "SELECT id_pokemon FROM ownedby WHERE name_pokemon = '{}' AND name_trainer='{}'".format(
            pokemon,
            trainer)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        result_id = cursor.fetchone()
    return result_id


def delete_pokemon_and_trainer_data_food(pokemon, trainer):
    query = """DELETE FROM ownedby
                WHERE name_trainer = '{}' AND name_pokemon = '{}'""".format(
            trainer,
            pokemon,
        )
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


