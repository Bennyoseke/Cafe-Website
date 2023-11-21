from flask import Flask, render_template, request, jsonify, url_for, redirect
import sqlite3
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)

# Define the path to the SQLite database
DATABASE = 'cafes.db'
Bootstrap5(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


class AddCafeForm(FlaskForm):
    cafe_name = StringField("Cafe Name:", validators = [DataRequired()])
    location = StringField("Location:", validators = [DataRequired()])
    image_url = StringField("Image URL:", validators = [DataRequired()])
    map_url = StringField("Map URL:", validators = [DataRequired(), URL()])
    sockets = StringField("Have Sockets: True/False", validators = [DataRequired()])
    toilet = StringField("Have Toilet: True/False", validators = [DataRequired()])
    wifi = StringField("Have WiFi: True/False", validators = [DataRequired()])
    calls = StringField("Can Take Calls: True/False", validators = [DataRequired()])
    submit = SubmitField("Submit Post")

# Function to connect to the database
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cafe')
    cafes = cursor.fetchall()
    db.close()
    cafes_with_boolean = [(cafe[0], cafe[1], cafe[2], cafe[3], cafe[4], bool(cafe[5]), bool(cafe[6]), bool(cafe[7]),
                           bool(cafe[8]), cafe[9], cafe[10]) for cafe in cafes]
    return render_template('index.html', cafes = cafes_with_boolean)

@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe_name.data
        location = form.location.data
        image = form.image_url.data
        map = form.map_url.data
        sockets = form.sockets.data
        toilet = form.toilet.data
        wifi = form.wifi.data
        calls = form.calls.data
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO cafe (name, location, img_url, map_url, has_sockets, has_toilet, has_wifi, can_take_calls) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (cafe_name, location, image, map, sockets, toilet, wifi, calls))
        db.commit()
        db.close()
        return redirect(url_for("home"))
    return render_template('add.html', form=form)

@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM cafe WHERE id = ?', (cafe_id,))
    db.commit()
    db.close()
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run(debug=True)

