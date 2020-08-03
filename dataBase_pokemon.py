import pymysql
import json
from pymysql import IntegrityError
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



# def select_id_owner(name, town):
#     query = "SELECT id FROM trainers WHERE name ='{}' AND town = '{}'".format(
#         name,
#         town
#     )
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchone()
#     except IntegrityError as error:
#         code, message = error.args
#         print("pokemon already exist")
#     return result['id']
#
# def select_id_from_type(name,url):
#     query = "SELECT id FROM type WHERE name ='{}' AND url = '{}'".format(
#         name,
#         url
#     )
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchone()
#     except IntegrityError as error:
#         code, message = error.args
#         print("pokemon already exist")
#     return result['id']

pokemon_file = open('pokimonim.json', 'r')
pokemon_data = json.load(pokemon_file)
# for pokemon in pokemon_data:
#     query = "INSERT into pokemon values ({},'{}',{},{})".format(
#         pokemon.get("id"),
#         pokemon.get("name"),
#         pokemon.get("height"),
#         pokemon.get("weight")
#     )
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             connection.commit()
#     except IntegrityError as error:
#         code, message = error.args
#         print("pokemon already exist")

for pokemon in pokemon_data:
    # for ownedBy in pokemon["ownedBy"]:
        # query = "INSERT into trainers(name,town) values ('{}','{}')".format(
        #     ownedBy.get("name"),
        #     ownedBy.get("town")
        # )
        # try:
        #     with connection.cursor() as cursor:
        #         cursor.execute(query)
        #         connection.commit()
        # except IntegrityError as error:
        #     code, message = error.args
        #     print("trainer already exist")

        # query = "INSERT into ownedby values ({},'{}')".format(
        #     pokemon.get("id"),
        #     ownedBy.get("name")
        # )
        # try:
        #     with connection.cursor() as cursor:
        #         cursor.execute(query)
        #         connection.commit()
        # except IntegrityError as error:
        #     code, message = error.args
        #     print("ownedBy already exist")

    #     query = "INSERT into type(name,url) values ('{}','{}')".format(
    #         type.get("type").get("name"),
    #         type.get("type").get("url"),
    #     )
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #             connection.commit()
    #     except IntegrityError as error:
    #         code, message = error.args
    #         print("type already exist")

        query = "INSERT into pokemontype values ({},'{}')".format(
            pokemon.get("id"),
            pokemon.get("type")
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except IntegrityError as error:
            code, message = error.args
            print("type already exist")

pokemon_file.close()
