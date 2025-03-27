from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)

    def __init__(self, original_url):
        self.original_url = original_url
        self.short_code = self.generate_short_code()

    def generate_short_code(self, length=6):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url  # Ensure valid URLs

        new_url = URL(original_url=original_url)
        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + new_url.short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return "URL not found!", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

