from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    
    sql = "SELECT * FROM Pokemon;"
    result = query_db(sql)
    return str(result)

@app.route("/Pokemon/<int:pokemon_num>")
def pokemon(pokemon_num):
    sql = """SELECT * FROM Pokemon 
         WHERE POkemon_num = ?;"""
    result = query_db(sql,(pokemon_num,),True)
    return str(result)
    


if __name__ == "__main__":
    app.run(debug=True) 