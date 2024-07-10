from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SECRET_KEY'] = 'hogehoge'  # セッション用の秘密鍵を設定
db = SQLAlchemy(app)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favorite_color = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

password = 'hogehoge'

ADMIN_PASSWORD = generate_password_hash(password)  # ハッシュ化されたパスワードを設定
print(ADMIN_PASSWORD)

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        favorite_color = request.form['favorite_color']
        feedback = request.form['feedback']
        
        new_response = Response(name=name, age=age, favorite_color=favorite_color, feedback=feedback)
        db.session.add(new_response)
        db.session.commit()
        
        return redirect(url_for('thank_you'))
    
    return render_template('survey.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if check_password_hash(ADMIN_PASSWORD, password):
            session['admin'] = True
            return redirect(url_for('admin_results'))
        else:
            return render_template('admin.html', error='パスワードが間違っています')
    return render_template('admin.html')

@app.route('/admin/results')
def admin_results():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    responses = Response.query.all()
    return render_template('admin_results.html', responses=responses)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('survey'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
