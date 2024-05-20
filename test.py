def search(name, genre, year_min, year_max, iswatched, country):
    try:
        query = f"""SELECT filtered_table2.Name, filtered_table2.Year, filtered_table2.Genre, 
            filtered_table2.County, filtered_table1.Grade 
        FROM 
            (SELECT * FROM {"films"} WHERE (Name = 'Any' OR Name = %s) AND (Genre = 'Any' OR Genre = %s) AND (%s >= Year) 
                    AND (Year <= %s) AND (Country = %s)) AS filtered_table2
        LEFT JOIN 
            (SELECT * FROM {"user"} WHERE ('false' = %s OR Grade != '')) AS filtered_table1
        ON 
            filtered_table1.Name = filtered_table2.Name"""
        cursor.execute(query, (name, genre, year_min, year_max, country, iswatched))
        result = cursor.fetchall()
        return result;
    except Error as e:
        print("Exception while search", e)
        return None


