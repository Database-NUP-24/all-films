mport mysql.connector

# Database connection details
db_config = {
    'user': 'film_user',
    'password': 'film_password',
    'host': 'localhost',
    'database': 'films_db'
}

# Data to be inserted
films = [
    ("Inception", "Science Fiction", "USA", 2010, "A mind-bending thriller where a thief enters people's dreams to steal secrets but is given the task to plant an idea instead. Directed by Christopher Nolan."),
    ("Spirited Away", "Fantasy", "Japan", 2001, "A young girl becomes trapped in a mysterious and magical world and must find a way to free herself and her parents. Directed by Hayao Miyazaki."),
    ("The Godfather", "Crime", "USA", 1972, "The saga of the powerful Italian-American crime family of Don Vito Corleone. Directed by Francis Ford Coppola."),
    ("Parasite", "Thriller", "South Korea", 2019, "A dark comedy about a poor family that schemes to become employed by a wealthy family by infiltrating their household. Directed by Bong Joon-ho."),
    ("The Grand Budapest Hotel", "Comedy", "USA", 2014, "A whimsical story about the adventures of a legendary concierge at a famous European hotel between the wars and the lobby boy who becomes his trusted friend. Directed by Wes Anderson."),
    ("The Shawshank Redemption", "Drama", "USA", 1994, "The story of a man sentenced to life in prison for a crime he didn't commit and his friendship with another inmate. Directed by Frank Darabont."),
    ("Pan's Labyrinth", "Fantasy", "Mexico", 2006, "A young girl in post-Civil War Spain escapes into a mythical world to escape the harsh realities of her life. Directed by Guillermo del Toro."),
    ("City of God", "Crime", "Brazil", 2002, "The story of two boys growing up in a violent neighborhood in Rio de Janeiro, and how their paths diverge. Directed by Fernando Meirelles."),
    ("Schindler's List", "Drama", "USA", 1993, "The true story of Oskar Schindler, who saved more than a thousand Jewish refugees during the Holocaust. Directed by Steven Spielberg."),
    ("The Dark Knight", "Action", "USA", 2008, "Batman faces the Joker, a criminal mastermind who plunges Gotham City into chaos. Directed by Christopher Nolan.")
]

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Create the films table if it doesn't exist with B-tree indexing on all columns
create_table_query = """
CREATE TABLE IF NOT EXISTS films (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    genre VARCHAR(255),
    country VARCHAR(255),
    year INT,
    description TEXT,
    INDEX idx_name (name) USING BTREE,
    INDEX idx_genre (genre) USING BTREE,
    INDEX idx_country (country) USING BTREE,
    INDEX idx_year (year) USING BTREE
)
"""

# Indexing: Implement B-tree or B+-tree indexing on at least one of the tables for efficient querying.


cursor.execute(create_table_query)

# Insert data into the films table
insert_query = """
INSERT INTO films (name, genre, country, year, description)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, films)

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Data inserted successfully.")
