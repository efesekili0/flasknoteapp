from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask import g

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'  # "note" adlı veritabanı
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True) #her not icin farkli kimlik tanitiyor
    content = db.Column(db.String(500), nullable=False)  # notta  ne yazior

#ana sayfa
@app.route('/', methods = ['GET', 'POST'])
def home():
    notlar = Notes.query.all()  # Tüm notları çek
    return render_template('index.html', notes=Notes.query.all())# burda sitede databasede olan tum notlari cektirip yeniletiosz

@app.route('/add_note', methods = ['GET','POST'])
def add_note():
    if request.method == 'POST':
        note_text = request.form.get['note'] # aldigin notu ismi note olarak kaydet
        new_note = Notes(content = note_text)
        db.session.add(new_note)
        db.session.commit()
    return render_template('index.html', notes=Notes.query.all())

@app.route('/delete_note/<int:note_id>', methods = ['POST', 'GET'])
def delete_note(note_id):
    del_note = Notes.query.get(note_id)
    db.session.delete(del_note)
    db.session.commit()
    return render_template('index.html',notes=Notes.query.all())

if __name__ == '__main__':
    app.run(debug=True)

