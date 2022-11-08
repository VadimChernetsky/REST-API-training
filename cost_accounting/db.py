import sqlite3

def read_sqlite_table():
    try:
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * from user_useruser"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        email_message = []
        for row in records:
            email_message.append(row[7])
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return email_message

email = read_sqlite_table()
