#OMDB API
'''
retrieves movies from MySQL, 
fetches OMDB data, 
recommends similar movies
'''
import os
import requests
import mysql.connector
from typing import Any
from dotenv import load_dotenv

load_dotenv()
APIKey = os.getenv("OMDB_API_KEY")
db_pass = os.getenv("MYSQL_PASS")


conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_pass,
    database="movies"
)
cursor=conn.cursor() #used to make queries


def getMoviesInDB()->list[Any]:
    cursor.execute("""SELECT title FROM movies""")
    results=cursor.fetchall()
    for movie in results:
        print(movie)
    return results

def getOMDBMovies(db:list[Any])->None:
    '''retrieve data for each movie in database'''
    #fetch API
    APIKey="3755f16b"
    for movie in db:
        title=movie
        url=f"http://www.omdbapi.com/?apikey={APIKey}&t={title}"
        response=requests.get(url).json()
        print(response)

def insertNewMovie(id:int, title:str, year:int, summary:str, revenue:int, rating:int, genre:str)->None:
    '''insert new movie into database'''
    cursor.execute(
        """INSERT INTO movies VALUES(%s,%s,%s,%s,%s,%s,%s)""", 
        (id, title, year, summary, revenue, rating, genre))
    
    conn.commit()

def analyzeDB()->list[Any]:
    '''taste profile of moview watcher'''
    preference:list[Any]=[]
    cursor.execute("""SELECT AVG(rating) FROM movies""")
    avgRating=cursor.fetchall()[0] #extract int val

    preference.append(avgRating)
    
    #return most popular genre
    cursor.execute("""SELECT genre 
                   FROM movies 
                   GROUP BY genre 
                   ORDER BY COUNT(genre) DESC
                   LIMIT 1""")
    topGenre=cursor.fetchall()[0] #extract string

    preference.append(topGenre)
    print(preference)
    
    return preference

def getOMDBMoviesRecs()->None:
    '''retrieve similar movies from preference'''
    #fetch API
    APIKey="3755f16b"
    prefGenre=analyzeDB()[1]
    '''
    cursor.execute("""SELECT title FROM movies WHERE genre=%s""",prefGenre)
    db=cursor.fetchall()
    for movie in db:
        title=movie
        url=f"http://www.omdbapi.com/?apikey={APIKey}&t={title}"
        response=requests.get(url).json()
        print(response)
        '''
    url=f"http://www.omdbapi.com/?apikey={APIKey}&s={prefGenre}"
    response=requests.get(url).json()
    #print(response)
    
    if response.get("Response") == "True":
        for movie in response.get("Search", []):
            print(f"You might also like: {movie.get('Title')}")
    else:
        print("No recommendations found.")



'''insertNewMovie(id=6, 
                title="Cinderella",
                year=1960,
                summary="This is a test row",
                revenue=800000,
                rating=3,
                genre="Family")'''

#allMovies=getMoviesInDB()
#getOMDBMovies(allMovies)
#analyzeDB()
getOMDBMoviesRecs()

cursor.close()
conn.close()
