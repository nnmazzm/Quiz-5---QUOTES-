import requests
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
db = SQLAlchemy(app)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    author = db.Column(db.String(100))

# Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quotes')
def quotes():
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    if response.status_code != 200:
        abort(500, description="Error fetching quote from the API")
    try:
        data = response.json()
        quote_text = data['quoteText']
        quote_author = data['quoteAuthor']
    except (ValueError, KeyError):
        abort(500, description="Invalid response format from the API") #ფუნქცია რომელიც არ გაგვიხილია ლექციაზე - abort()
    return render_template('quotes.html', quote_text=quote_text, quote_author=quote_author)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        text = request.form.get('text')
        author = request.form.get('author')
        if not text or not author:
            abort(400, description="Both text and author fields are required") #ფუნქცია რომელიც არ გაგვიხილია ლექციაზე - abort()
        new_quote = Quote(text=text, author=author)
        db.session.add(new_quote)
        db.session.commit()
        flash('Quote added successfully!', 'success')
        return redirect(url_for('quotes'))
    return render_template('add_quote.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
