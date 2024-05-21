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


def search(name, genre, year_min, year_max, iswatched, country):
    if name == '':
        name = "any"
    if iswatched:
        query = f"""SELECT filtered_table2.Name, filtered_table2.Genre,
                            filtered_table2.Country, filtered_table2.Year, filtered_table2.Description, filtered_table1.Grade
                        FROM
                            (SELECT * FROM {table2} WHERE (%s = 'any' OR Name LIKE '{name}%') AND (%s = 'any' OR Genre = %s) AND (%s < Year)
                                    AND (Year < %s) AND (%s = 'any' OR Country = %s)) AS filtered_table2
                        INNER JOIN 
                            (SELECT * FROM {table1}) AS filtered_table1
                        ON
                            filtered_table1.Name = filtered_table2.Name"""
    else:
        query = f"""SELECT filtered_table2.Name, filtered_table2.Genre,
                                    filtered_table2.Country, filtered_table2.Year, filtered_table2.Description, filtered_table1.Grade
                                FROM
                                    (SELECT * FROM {table2} WHERE (%s = 'any' OR Name LIKE '{name}%') AND (%s = 'any' OR Genre = %s) AND (%s < Year)
                                            AND (Year < %s) AND (%s = 'any' OR Country = %s)) AS filtered_table2
                                LEFT JOIN
                                    (SELECT * FROM {table1}) AS filtered_table1
                                ON
                                    filtered_table1.Name = filtered_table2.Name"""

    connection, cursor = open_connection()
    cursor.execute(query, (name, genre, genre, int(year_min), int(year_max), country, country))
    result = cursor.fetchall()  # Fetch results before closing cursor
    cursor.close()
    connection.close()
    result_dicts = []
    result.sort()
    for x in result[0: len(result): 2]:
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

