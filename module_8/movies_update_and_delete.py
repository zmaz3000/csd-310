#Zachary Maziarz - MySQL Database queries Module 8

import mysql.connector
from mysql.connector import errorcode

config = {
    "user" : "movies_user",
    "password" : "popcorn",
    "host" : "127.0.0.1",
    "database" : "movies",
    "raise_on_warnings" : True 
}

db = mysql.connector.connect(**config)
cursor = db.cursor()



def show_films(cursor, title):    #Studio Query
    
    cursor.execute(
    """
    SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name'
    FROM film  
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    )

    films = cursor.fetchall()
    print("\n -- {} --".format(title))


    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))
    



show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

db.close()