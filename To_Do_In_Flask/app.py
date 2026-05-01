import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 🔹 Create DB + table if not exists
def init_db():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 🔹 Home route
@app.route("/")
def index():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

# 🔹 Add task
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        conn = sqlite3.connect("todo.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect("/")

# 🔹 Delete task
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)