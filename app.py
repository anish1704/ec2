from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, default="")
    phone_number = db.Column(db.String(20), nullable=False, default="")
    password = db.Column(db.String(60), nullable=False, default="")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email', '')
        phone_number = request.form.get('phone_number', '')
        user = User(name=name, email=email, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('page2'))
    return render_template('page1.html')

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        password = request.form.get('password', '')
        user = User.query.order_by(User.id.desc()).first()
        user.password = password
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('page2.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
