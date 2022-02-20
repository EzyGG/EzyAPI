import mysql.connector


connection = mysql.connector.connect(host="luzog.xyz", user="dev", password="root", database="ezy")
cursor = connection.cursor()


def execute(operation, param: tuple = (), multi: bool = False):
    return cursor.execute(operation, param, multi)


def commit():
    return connection.commit()


def fetch(size: int = None):
    return cursor.fetchall() if size is None else cursor.fetchone() if size == 1 else cursor.fetchmany(size)


def close():
    return connection.close()
