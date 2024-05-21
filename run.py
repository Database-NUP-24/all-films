from flask import Flask, render_template, request, jsonify
import database_manager

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
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'checkbox':
        checkbox_state = data.get('checked', False)
        print(f"Received checkbox update: {'Checked' if checkbox_state else 'Unchecked'}")
        iswatched = checkbox_state
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'select_min':
        selected_value = data.get('value', '')
        print(f"Received select min update: {selected_value}")
        year_min = int(selected_value)
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'select_max':
        selected_value = data.get('value', '')
        print(f"Received select max update: {selected_value}")
        year_max = int(selected_value)
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'grade':
        selected_grade = data.get('grade', '')
        selected_film = data.get('film', '')
        print(f"Received grade {selected_grade} for {selected_film}")
        database_manager.add_to_table1(selected_film, selected_grade)
        return jsonify(status="success", type="grade", value=selected_grade)

    elif update_type == 'genre':
        selected_genre = data.get('value', '')
        print(f"Received genre {selected_genre}")
        genre = selected_genre
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    elif update_type == 'country':
        selected_country = data.get('value', '')
        print(f"Received country {selected_country}")
        country = selected_country
        return database_manager.search(name, genre, year_min, year_max, iswatched, country)

    else:
        return jsonify(status="error", message="Unknown update type"), 400


if __name__ == '__main__':
    app.run(debug=True)
