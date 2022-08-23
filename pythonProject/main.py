import pandas as pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlite3 as sql
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
engine = create_engine('sqlite://', echo=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    df = pd.read_csv(request.files.get('file'))
    return render_template('upload.html', shape=df.shape, columns=df.columns.values)


@app.route('/test')
def test():
    df0 = pd.DataFrame({'name': ['user01', 'user02', 'user03']})
    df0.to_sql('users', con=engine)
    return engine.execute("SELECT * FROM users").fetchall()


@app.route('/user_form')
def new_user():
    return render_template('user.html')


@app.route('/user_info', methods=['POST', 'GET'])
def user_info():
    if request.method == 'POST':
        try:
            user_email = request.form['user_email']
            user_name = request.form['user_name']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO users (email, name) VALUES (?,?)", (user_email, user_name))
                msg = "Success"

        except:
            con.rollback()
            msg = "error"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")  # database.db파일에 접근.
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


if __name__ == "__main__":
    app.run()
