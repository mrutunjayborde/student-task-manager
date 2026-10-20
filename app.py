from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Demo tasks are kept in memory; restarting the app resets them.
tasks = [
    {"id": 1, "title": "Complete Cloud Computing notes", "done": False},
    {"id": 2, "title": "Practise Java programming", "done": True},
]
next_id = 3


@app.get("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.post("/add")
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title, "done": False})
        next_id += 1
    return redirect(url_for("index"))


@app.post("/toggle/<int:task_id>")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
