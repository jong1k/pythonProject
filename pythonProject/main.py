import pandas as pd
from flask import Flask, request, render_template
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///csv.db', echo=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files['file']
    f_name = f.filename.split(".")[0]

    df = pd.read_csv(f)
    df.to_sql(f_name, con=engine, if_exists='replace')

    upload_result = 'File uploaded to DB("csv.db" file). The table name is ' + f_name + ' and its shape is ' + str(
        df.shape)
    return render_template('index.html', uploadResult=upload_result)


@app.route("/query", methods=["POST"])
def query():
    q = request.form['query']
    query_result = str(engine.execute(str(q)).fetchall())
    return render_template('index.html', queryResult=query_result)


if __name__ == "__main__":
    app.run()
