from django.db import connections
from cx_Oracle import LOB

def custom_query(query, filter=[], str_con='default'):
    """
    Returno custom query (SQLRaw)
    :param query: SQL Instruction
    :param filter: Filter to Apply (Array)
    :param str_con: String database connection
    :return: Dict
    """
    with connections[str_con].cursor() as cursor:
        cursor.execute(query, filter)
        columns = [col[0].lower() for col in cursor.description]
        data = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        for i in enumerate(data):
            for c in columns:
                if type(data[i[0]][c]) == LOB:
                    data[i[0]][c] = data[i[0]][c].read()

        return data