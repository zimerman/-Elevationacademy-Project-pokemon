import json
from pymysql import IntegrityError
from conect import connection

pokemon_file = open('pokemon_data.json', 'r')
pokemon_data = json.load(pokemon_file)

sensitive_food_file = open('food_data.json', 'r')
sensitive_food_data = json.load(sensitive_food_file)
for pokemon in pokemon_data:
    query = "INSERT into pokemon values ({},'{}',{},{})".format(
        pokemon.get("id"),
        pokemon.get("name"),
        pokemon.get("height"),
        pokemon.get("weight")
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except IntegrityError as error:
        code, message = error.args
        print("pokemon already exist")
    query = "INSERT into type values ('{}')".format(pokemon.get("type"))
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except IntegrityError as error:
        code, message = error.args
        print("type already exist")
    for ownedBy in pokemon["ownedBy"]:
        query = "INSERT into trainers(name,town) values ('{}','{}')".format(
            ownedBy.get("name"),
            ownedBy.get("town")
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except IntegrityError as error:
            code, message = error.args
            print("trainer already exist")
        query = "INSERT into ownedby values ({},'{}','{}')".format(
            pokemon.get("id"),
            pokemon.get("name"),
            ownedBy.get("name")
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except IntegrityError as error:
            code, message = error.args
            print("ownedBy already exist")
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
for sensitive in sensitive_food_data:
    for food in sensitive.get("food"):
        query = "INSERT into food values ('{}')".format(food)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except IntegrityError as error:
            code, message = error.args
            print("type already exist")
        query = "INSERT into sensitive_food values ('{}','{}')".format(
            food,
            sensitive.get("type")
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except IntegrityError as error:
            code, message = error.args
            print("type already exist")
for type in ["flying", "dark", "steel"]:
    query = "INSERT into type values ('{}')".format(type)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except IntegrityError as error:
        code, message = error.args
        print("type already exist")


pokemon_file.close()
