import pandas as pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlite3 as sql
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECRET_KEY'] = "random string"

engine = create_engine('sqlite://', echo=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    df = pd.read_csv(request.files.get('file'))
    df.to_sql('csv1', con=engine)
    return str(engine.execute("SELECT * FROM csv1").fetchall())
    # return render_template('upload.html', shape=df.shape, columns=df.columns.values)


if __name__ == "__main__":
    app.run()
