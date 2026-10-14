
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "clave-local-de-desarrollo"
)
CSRFProtect(app)


class Stack:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        return len(self.items) >= self.capacity

    def push(self, item):
        if self.is_full():
            return False
        self.items.append(item)
        return True

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def pop(self):
        return None if self.is_empty() else self.items.pop()


def get_stack():
    capacity = session.get("capacity", 5)
    items = session.get("stack", [])

    if not isinstance(capacity, int) or not 1 <= capacity <= 100:
        capacity = 5

    if not isinstance(items, list):
        items = []

    stack = Stack(capacity)
    stack.items = [str(item) for item in items]
    stack.items = stack.items[-capacity:]
    return stack


def save_stack(stack):
    session["stack"] = stack.items
    session["capacity"] = stack.capacity


@app.get("/")
def index():
    stack = get_stack()
    save_stack(stack)

    return render_template(
        "index.html",
        items=list(reversed(stack.items)),
        capacity=stack.capacity,
        count=len(stack.items),
        available=stack.capacity - len(stack.items),
        top=stack.peek(),
        is_empty=stack.is_empty(),
        is_full=stack.is_full(),
    )


@app.post("/push")
def push():
    value = request.form.get("item", "").strip()
    stack = get_stack()

    if not value:
        flash("Escribe un elemento.", "warning")
    elif len(value) > 100:
        flash("El elemento no puede superar 100 caracteres.", "warning")
    elif stack.push(value):
        save_stack(stack)
        flash("Elemento apilado correctamente.", "success")
    else:
        flash("La pila está llena.", "danger")

    return redirect(url_for("index"))


@app.post("/pop")
def pop():
    stack = get_stack()
    item = stack.pop()

    if item is None:
        flash("La pila está vacía.", "warning")
    else:
        save_stack(stack)
        flash(f"Elemento '{item}' desapilado.", "success")

    return redirect(url_for("index"))


@app.post("/clear")
def clear():
    session["stack"] = []
    flash("La pila se ha vaciado correctamente.", "success")
    return redirect(url_for("index"))


@app.post("/configure")
def configure():
    try:
        capacity = int(request.form.get("capacity", ""))
    except (ValueError, TypeError):
        flash("Introduce una capacidad válida.", "danger")
        return redirect(url_for("index"))

    if not 1 <= capacity <= 100:
        flash("La capacidad debe estar entre 1 y 100.", "danger")
        return redirect(url_for("index"))

    stack = get_stack()

    if not stack.is_empty():
        flash("Vacía la pila antes de cambiar la capacidad.", "warning")
    else:
        session["capacity"] = capacity
        session["stack"] = []
        flash("Capacidad actualizada.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
