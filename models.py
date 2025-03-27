from flask import Flask
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")
