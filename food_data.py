from conect import connection


def get_sensitive_food(list_type):
    list_food = []
    for type in list_type:
        query = """SELECT name_food FROM sensitive_food WHERE name_type = '{}'""".format(
            type
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        list_food.append(result)
    return list_food
