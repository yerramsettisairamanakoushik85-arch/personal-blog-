from flask import Flask, render_template, request, redirect, session
import os, json

app = Flask(__name__)
app.secret_key = "blog-secret"
ARTICLES = "articles"

@app.route("/")
def home():
    posts = []
    for file in os.listdir(ARTICLES):
        with open(os.path.join(ARTICLES, file)) as f:
            posts.append(json.load(f))
    return render_template("home.html", posts=posts)

@app.route("/article/<name>")
def article(name):
    with open(os.path.join(ARTICLES, name)) as f:
        post = json.load(f)
    return render_template("article.html", post=post)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")
    posts = os.listdir(ARTICLES)
    return render_template("admin.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "admin" not in session:
        return redirect("/login")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]
        name = title.lower().replace(" ", "-") + ".json"
        with open(os.path.join(ARTICLES, name), "w") as f:
            json.dump({"title": title, "content": content, "date": date}, f)
        return redirect("/admin")
    return render_template("add.html")
@app.route("/edit/<name>", methods=["GET", "POST"])
def edit(name):
    if "admin" not in session:
        return redirect("/login")

    path = os.path.join(ARTICLES, name)

    with open(path) as f:
        post = json.load(f)

    if request.method == "POST":
        post["title"] = request.form["title"]
        post["content"] = request.form["content"]
        post["date"] = request.form["date"]

        with open(path, "w") as f:
            json.dump(post, f)

        return redirect("/admin")

    return render_template("edit.html", post=post, name=name)
@app.route("/delete/<name>")
def delete(name):
    if "admin" not in session:
        return redirect("/login")
    os.remove(os.path.join(ARTICLES, name))
    return redirect("/admin")

if __name__ == "__main__":
    app.run(port=5000, debug=True)