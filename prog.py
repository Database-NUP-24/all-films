from flask import Flask, render_template, request, jsonify
import json
import os
import databaseManager

app = Flask(__name__)

pathToFilms = "films.json"
pathToScores = "scores.json"

genre = "any"
country = "any"
year_min = 1900
year_max = 2024
name = ""
iswatched = False

@app.route('/')
def index():
    return render_template('page.html')

@app.route('/update', methods=['POST'])
def update():
    global name, genre, year_min, year_max, iswatched, country
    data = request.json
    update_type = data.get('type')

    if update_type == 'text':
        new_text = data.get('text', '')
        print(f"Received text update: {new_text}")
        name = new_text
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'checkbox':
        checkbox_state = data.get('checked', False)
        print(f"Received checkbox update: {'Checked' if checkbox_state else 'Unchecked'}")
        iswatched = checkbox_state
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'select_min':
        selected_value = data.get('value', '')
        print(f"Received select min update: {selected_value}")
        year_min = int(selected_value)
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'select_max':
        selected_value = data.get('value', '')
        print(f"Received select max update: {selected_value}")
        year_max = int(selected_value)
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'grade':
        selected_grade = data.get('grade', '')
        selected_film = data.get('film', '')
        print(f"Received grade {selected_grade} for {selected_film}")
        databaseManager.add_to_table1(selected_film, selected_grade)
        return jsonify(status="success", type="grade", value=selected_grade)

    elif update_type == 'genre':
        selected_genre = data.get('value', '')
        print(f"Received genre {selected_genre}")
        genre = selected_genre
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'country':
        selected_country = data.get('value', '')
        print(f"Received country {selected_country}")
        country = selected_country
        return databaseManager.search(name, genre, year_min, year_max, iswatched, country)

    else:
        return jsonify(status="error", message="Unknown update type"), 400

# def search(name, genre = "", yearFrom = 0, yearTo = 2024, isWatched = False, country = ""):
#
#     with open(pathToScores, "r", encoding="utf-8") as file1:
#         scores_data = json.load(file1)
#
#     with open(pathToFilms, "r", encoding="utf-8") as file2:
#         films_data = json.load(file2)
#     name = name.lower()
#     watched_films = [obj for obj in scores_data]
#     matching_films = [
#         film for film in films_data
#         if film["title"].lower().startswith(name) and
#             film["year"] >= yearFrom and
#             film["year"] <= yearTo and
#             (film["genre"] == genre or genre=="any") and
#             (film["country"] == country or country=="any") and
#            (film["title"].lower() in [obj["name"].lower() for obj in watched_films] or not isWatched)
#     ]
#     for i in range(len(matching_films)):
#         curGrade = "?"
#         for obj in watched_films:
#             if obj["name"].lower() == matching_films[i]["title"].lower():
#                 curGrade = obj["score"]
#         matching_films[i]["grade"] = curGrade
#     return jsonify(results=matching_films)
# def score(name,score):
#
#     if os.path.exists(pathToScores) and os.path.getsize(pathToScores) > 0:
#         # Load existing data
#         with open(pathToScores, "r", encoding="utf-8") as file:
#             data = json.load(file)
#     else:
#         # Initialize an empty list if file is empty or does not exist
#         data = []
#     found = False
#     for i in range(len(data)):
#         if data[i]["name"].lower() == name.lower():
#             found = True
#             data[i]["score"] = score
#             break
#
#     if not found:
#         data.append({"name":name, "score":score})
#     with open(pathToScores, "w", encoding="utf-8") as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
