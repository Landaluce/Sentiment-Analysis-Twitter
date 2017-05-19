from app import app
from flask import render_template, request
from TwitterAPI import get_sentiments


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'reset' in request.form:
            return render_template("index.html")
        search_query = request.form['search_query']
        quantity = request.form['quantity']
        results, zipped = get_sentiments(search_query, int(quantity))
        return render_template("results.html", results=results, zipped=zipped)
    return render_template("index.html")
