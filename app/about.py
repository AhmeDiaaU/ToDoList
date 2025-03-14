from flask import Flask, render_template

about_bp = Flask('about', __name__, url_prefix='/about')

@about_bp.route("/")
def about():
    return render_template("about.html")