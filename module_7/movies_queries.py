#Zachary Maziarz - MySQL Database queries Module 7

import mysql.connector
from mysql.connector import errorcode

config = {
    "user" : "movies_user",
    "password" : "popcorn",
    "host" : "127.0.0.1",
    "database" : "movies",
    "raise_on_warnings" : True 
}

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySQL on host {} with database {}". format(config["user"], config["host"], config["database"]))
    cursor = db.cursor()
    #Studio Query
    cursor.execute("SELECT * FROM studio")
    records = cursor.fetchall()
    print("-- DISPLAYING Studio RECORDS --")
    for record in records:
        print(f"Studio ID: {record[0]}")
        print(f"Studio Name: {record[1]}\n")
    # Genre Query
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    print("-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}\n")
    #Film with 2 hours runtime query
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    films = cursor.fetchall()
    print("-- DISPLAYING Short Film RECORDS --")
    for film in films:
        print(f"Film Name: {film[0]}")
        print(f"Runtime: {film[1]}\n")
    #Film Names and Directors Ordered by director
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    directors = cursor.fetchall()
    print("-- DISPLAYING Director RECORDS in ORDER --")
    for director in directors:
        print(f"Film Name: {director[0]}")
        print(f"Director: {director[1]}\n")
    

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")
    
    else:
        print(err)
finally:
    db.close()