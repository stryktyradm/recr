from app.main import main
from flask import request, render_template


@main.route("/", methods=["GET"])
def index():
    name = request.args.get("name")
    message = request.args.get("message")
    return render_template("index.html", name=name, message=message)