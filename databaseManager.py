import mysql.connector
from flask import Flask, render_template, request, jsonify
from mysql.connector import Error

table1 = "User"
table2 = "films"

def open_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='film_user',
        password='film_password',
        database='films_db'
    )
    cursor = connection.cursor()
    return connection, cursor

def add_to_table1(name, grade):
    connection, cursor = open_connection()
    cursor.execute(f"INSERT INTO `{table1}` (Name, Grade) VALUES (%s, %s)", (name, grade))
    connection.commit()
    cursor.close()
    connection.close()

# def add_to_table2(name, year, genre, country):
#     connection, cursor = open_connection()
#     cursor.execute(f"INSERT INTO `{table2}` (Name, Year, Genre, Country) VALUES (%s, %s, %s, %s)",
#                    (name, year, genre, country))
#     connection.commit()
#     cursor.close()
#     connection.close()

# def search_by_name(name):
#     connection, cursor = open_connection()
#     query = f"""
#                     SELECT t1.Name, t1.Year, t2.Genre, t2.Country
#                     FROM `{table1}` t1
#                     JOIN `{table2}` t2 ON t1.Name = t2.Name
#                     WHERE t1.Name = %s
#                     """
#     cursor.execute(query, (name,))
#     result = cursor.fetchall()
#     connection.commit()
#     cursor.close()
#     connection.close()
#
#     return result

def search(name, genre, year_min, year_max, iswatched, country):
    iswatched = str(iswatched).lower()
    if name == '':
        name = "any"
    print(year_min, year_max, "years")
    # query = f"""SELECT filtered_table2.Name, filtered_table2.Genre,
    #                 filtered_table2.Country, filtered_table2.Year, filtered_table2.Description, filtered_table1.Grade
    #             FROM
    #                 (SELECT * FROM {table2} WHERE ({name} = 'any' OR Name = {name}) AND ({genre} = 'any' OR Genre = {genre}) AND ({year_min} < Year)
    #                         AND (Year < {year_max}) AND (Country = {country})) AS filtered_table2
    #             LEFT JOIN
    #                 (SELECT * FROM {table1} WHERE ('false' = {iswatched} OR Grade != '')) AS filtered_table1
    #             ON
    #                 filtered_table1.Name = filtered_table2.Name"""

    query = f"""SELECT filtered_table2.Name, filtered_table2.Genre,
                        filtered_table2.Country, filtered_table2.Year, filtered_table2.Description, filtered_table1.Grade
                    FROM
                        (SELECT * FROM {table2} WHERE (%s = 'any' OR Name = %s) AND (%s = 'any' OR Genre = %s) AND (%s < Year)
                                AND (Year < %s) AND (%s = 'any' OR Country = %s)) AS filtered_table2
                    LEFT JOIN
                        (SELECT * FROM {table1} WHERE ('false' = %s OR Grade != '')) AS filtered_table1
                    ON
                        filtered_table1.Name = filtered_table2.Name"""


    print(query)
    # query = f"""SELECT filtered_table2.Name, filtered_table2.Genre,
    #                     filtered_table2.Country, filtered_table2.Year, filtered_table2.Description, filtered_table1.Grade
    #                 FROM
    #                     (SELECT * FROM {table2} WHERE (%s = '' OR Name = %s) AND (%s = 'any' OR Genre = %s) AND (Country = %s)) AS filtered_table2
    #                 LEFT JOIN
    #                     (SELECT * FROM {table1} WHERE ('false' = %s OR Grade != '')) AS filtered_table1
    #                 ON
    #                     filtered_table1.Name = filtered_table2.Name"""
    connection, cursor = open_connection()
    # query = f"""SELECT * from {table2}"""
    #cursor.execute(query)
    cursor.execute(query, (name, name, genre, genre, int(year_min), int(year_max), country, country, iswatched))
    #cursor.execute(query, (country,))
    result = cursor.fetchall()  # Fetch results before closing cursor
    cursor.close()
    connection.close()
    print(result)
    result_dicts = []
    for x in result[:len(result) // 2]:
        new_d = {
            "title": x[0],
            "genre": x[1],
            "country": x[2],
            "year": x[3],
            "description": x[4],
            "grade": x[5],
        }
        result_dicts.append(new_d)
    return jsonify(results=result_dicts)

