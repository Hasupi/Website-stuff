from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)
connection = sqlite3.connect('arcaea_attempt2.db', check_same_thread=False)
cur = connection.cursor()


@app.route("/")
def home():
    cur.execute("""SELECT *, (CASE WHEN FTR = '9+' THEN 9.5 WHEN FTR = '10+' THEN 10.5 ELSE FTR END) AS sort FROM Song ORDER BY sort DESC""")
    Songs = cur.fetchall()
    return render_template("index.html", Songs=Songs)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/packentry/<int:id>")
def packentry(id):
    cur.execute("SELECT * FROM Packs WHERE id = ?", (id,))
    packentry = cur.fetchone()
    cur.execute("SELECT * FROM Song WHERE Packs = ?", (id,))
    songs = cur.fetchall()
    print(songs)
    return render_template("packentry.html", pack = packentry, songs=songs)


@app.route("/packs")
def packs():
    cur.execute("""SELECT Packs.id,
                        pack_name,
                        Image
                    From Packs""")
    p = cur.fetchall()
    return render_template("packs.html", packs=p,)


@app.route("/songs/<int:id>")
def songs(id):
    cur.execute("SELECT * FROM Song WHERE id = ?", (id,))
    song = cur.fetchone()
    return render_template("song.html", song=song)
    

@app.errorhandler(404)  
def die(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug="true", host="0.0.0.0", port="8000")
    
    