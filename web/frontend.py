from flask import Flask, render_template, request, Response, send_file, Blueprint

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@frontend.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@frontend.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")